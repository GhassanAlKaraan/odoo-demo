from odoo import models, fields
from odoo.exceptions import UserError
import logging
import requests

_logger = logging.getLogger(__name__)


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    partner_id = fields.Many2one('res.partner', string='Location Partner')

    # 1
    def get_api_key_and_location(self, show_error=False):
        # Fetch the API key from the configuration
        api_key = self.env["ir.config_parameter"].sudo().get_param("flower_shop.weather_api_key")

        # Check if the API key is not set or empty
        if api_key == "unset" or not api_key:
            error_msg = "Weather API key is not set in system parameters."
            _logger.error(error_msg)
            if show_error:
                raise UserError(error_msg)
            return None, None, None

        # Check if the partner_id is set and if latitude and longitude are available
        if not self.partner_id or not self.partner_id.partner_latitude or not self.partner_id.partner_longitude:
            error_msg = "Location data not available for the warehouse."
            _logger.error(error_msg)
            if show_error:
                raise UserError(error_msg)
            return None, None, None

        # Return the API key along with the latitude and longitude
        return api_key, self.partner_id.partner_latitude, self.partner_id.partner_longitude

    # 2
    def fetch_weather(self):
        self.ensure_one()  # ensure that the method is called on a single record
        api_key, lat, lon = self._get_api_key_and_location(show_error=True)
        if not api_key or not lat or not lon:
            raise UserError("Required parameters (API key, latitude, longitude) are missing or incomplete.")

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()

            # Creating the weather record
            weather_record = {
                'warehouse_id': self.ids[0],
                'temperature': data['main']['temp'],
                'pressure': data['main']['pressure'],
                'humidity': data['main']['humidity'] / 100,  # Convert to percentage
                'wind_speed': data['wind']['speed'],
                'rain_volume': data.get('rain', {}).get('1h', 0),
                'description': data['weather'][0]['description'],
                'capture_time': fields.Datetime.now(),  # Capture the current time of the data fetch
            }
            self.env['stock.warehouse.weather'].create(weather_record)
        except requests.HTTPError as e:
            _logger.error(f"HTTP Error occurred: {e}")
            raise UserError(f"Failed to fetch weather data: {e}")
        except requests.RequestException as e:
            _logger.error(f"Request failed: {e}")
            raise UserError(f"Error during weather data request: {e}")
        except Exception as e:
            _logger.error(f"An unexpected error occurred: {e}")
            raise UserError(f"An unexpected error occurred: {e}")

    # 3
    def get_weather_all_warehouses(self):
        for warehouse in self.search([]):
            warehouse.fetch_weather(show_error=False)

    # 4
    def get_forecast_all_warehouses(self, show_error=True):
        flower_serials_to_water = self.env["stock.lot"]
        for warehouse in self.search([]):  # Assuming you want to run this for all warehouses
            api_key, lat, lon = warehouse.get_api_key_and_location(show_error)
            if not api_key or not lat or not lon:
                continue  # Skip this warehouse if the API key or location data is missing

            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()  # Check for HTTP errors
                entries = response.json()
                is_rainy_today = False

                # Check only the first 4 items in the list from 9 AM to 6 PM
                for entry in entries['list'][:4]:
                    rain = entry.get("rain", {}).get("3h", 0)
                    if rain > 0.2:
                        is_rainy_today = True
                        break

                if is_rainy_today:
                    flower_products = self.env["product.product"].search([("is_flower", "=", True)])
                    quants = self.env["stock.quant"].search([
                        ("product_id", "in", flower_products.ids),
                        ("location_id", "=", warehouse.lot_stock_id.id)
                    ])
                    flower_serials_to_water |= quants.mapped('lot_id')

            except requests.HTTPError as e:
                _logger.error(f"HTTP Error for warehouse {warehouse.name}: {e}")
                if show_error:
                    raise UserError(f"HTTP Error for warehouse {warehouse.name}: {e}")
            except requests.RequestException as e:
                _logger.error(f"Request Error for warehouse {warehouse.name}: {e}")
                if show_error:
                    raise UserError(f"Request Error for warehouse {warehouse.name}: {e}")
            except Exception as e:
                _logger.error(f"Unexpected error for warehouse {warehouse.name}: {e}")
                if show_error:
                    raise UserError(f"Unexpected error for warehouse {warehouse.name}: {e}")

        # Watering the flowers
        for flower_serial in flower_serials_to_water:
            self.env["flower_shop.flower.water"].create({
                "serial_id": flower_serial.id,
            })
