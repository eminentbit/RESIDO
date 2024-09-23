from django.conf import settings
from django.shortcuts import redirect
from urllib.parse import urlencode
import requests, json, datetime
from humanfriendly import format_timespan
from django.http import JsonResponse


def FormErrors(*args):
    '''
    Handles form error that are passed back to AJAX calls
    '''
    message = ''
    for f in args:
        if f.errors:
            message = f.errors.as_text()
    return message

def reCAPTCHAValidation(token):

    '''reCAPTCHA validation'''
    result = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.RECAPTCHA_KEY,
            'response': token
        }
    )
    return result.json()

def RedirectParams(**kwargs):
    '''
    Used to append url parameters when redirecting users
    '''
    url = kwargs.get('url')
    params = kwargs.get('params')
    response = redirect(url)
    if params:
        query_string = urlencode(params)
        response['Location'] += '?' + query_string
    return response

class AjaxFormMixin(object):
    '''
    Mixin to ajaxify django form - can be over written in view by callback
    '''

    def form_invalid(self, form):
        response = super(AjaxFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            message = FormErrors(form)
            return JsonResponse({'result': 'Error', 'message': message})
        
    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            form.save()
            return JsonResponse({'result': 'Success', 'message': ''})
        return response
    

def Directions(*args, **kwargs):
    '''
    Handles directions from Google
    '''

    lat_a = kwargs.get('lat_a')
    long_a = kwargs.get('long_a')
    lat_b = kwargs.get('lat_b')
    long_b = kwargs.get('long_b')
    lat_c = kwargs.get('lat_c')
    long_c = kwargs.get('long_c')
    lat_d = kwargs.get('lat_d')
    long_d = kwargs.get('long_d')

    origin = f'{lat_a},{long_a}'
    destination = f'{lat_b},{long_b}'
    waypoints = f'{lat_c},{long_c}|{lat_d},{long_d}'

    result = requests.get(
        'https://maps.googleapis.com/maps/api/directions/json?',
        params={
            'origin': origin,
            'destination': destination,
            'waypoints': waypoints,
            'key': settings.GOOGLE_API_KEY
        }
    )
    directions = result.json()

    if directions['status'] == 'OK':
        routes = directions['routes'][0]['legs']

        distance = 0
        duration = 0
        route_list = []

        for route in routes:
            distance += int(route['distance']['value'])
            duration += int(route['duration']['value'])

            steps = []
            for step in route['steps']:
                steps.append({
                    'instruction': step['html_instructions'],
                    'distance': step['distance']['text'],
                    'duration': step['duration']['text']
                })

            route_step = {
                'origin': route['start_address'],
                'destination': route['end_address'],
                'distance': route['distance']['text'],
                'duration': route['duration']['text'],
                'steps': steps
            }

            route_list.append(route_step)

        return {
            'origin': origin,
            'destination': destination,
            'distance': f'{round(distance/1000, 2)} Km',
            'duration': format_timespan(duration),
            'route': route_list
        }
    else:
        return {'error': 'Unable to fetch directions.'}