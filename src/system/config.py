from time import timezone


config_matrix = {
    'width' : 64,
    'height' : 32,
}

config_notification= {
    'alert_icon' : "O" #O for a circle, Q for a heart
}

secrets = {
    'ssid' : 'jgage_netgear',
    'password' : 'melodicboat789',
    'timezone' : "America/Chicago", # http://worldtimeapi.org/timezones
    'api_read-unread' : 'https://a4lrurckzb.execute-api.us-east-2.amazonaws.com/prod/events/read-unread'
}

package = {
    "version" : "v1.0.0"
}

config_timezone = {
    "offsets" : [1, 2, -5]
}