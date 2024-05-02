from odoo import fields, models


# URI: api.openweathermap.org
#
# Key: 56d63573aa9aaee48654f8a182581103
#
# URL Call: api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=56d63573aa9aaee48654f8a182581103
#
# Documentation: https://openweathermap.org/api

class StockWarehouseWeather(models.Model):
    _name = 'stock.warehouse.weather'
    _description = 'Warehouse Weather'

    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', required=True, ondelete='cascade')
    temperature = fields.Float(string='Temperature (°C)')
    pressure = fields.Float(string='Pressure (hPa)')
    humidity = fields.Float(string='Humidity (%)')
    wind_speed = fields.Float(string='Wind Speed (km/h)')
    rain_volume = fields.Float(string='Rain Volume (mm)', help="Rain volume for the past hour")
    description = fields.Char(string='Weather Description')
    capture_time = fields.Datetime(string='Capture Time', default=fields.Datetime.now)
