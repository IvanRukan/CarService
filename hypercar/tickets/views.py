from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import RedirectView
from django.shortcuts import redirect
from collections import deque

data = {'oil': [], 'tires': [], 'diagnostics': []}
numbers = [deque(), deque(), deque()]
ticket_number = 1
result_num = 1
clicked = False


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse()
        response.write('<h2>Welcome to the Hypercar Service!</h2>')
        return response


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html')


class ServiceViewOil(View):
    def get(self, request, *args, **kwargs):
        global ticket_number
        numbers[0].append(ticket_number)
        ticket_number += 1
        data['oil'].append(2)
        number = len(data['oil'])
        min_to_wait = sum(data['oil']) - 2
        return render(request, 'tickets/service.html', context={'number': number, 'minutes': min_to_wait})


class ServiceViewTires(View):
    def get(self, request, *args, **kwargs):
        global ticket_number
        numbers[1].append(ticket_number)
        ticket_number += 1
        data['tires'].append(5)
        number = len(data['tires'])
        min_to_wait = sum(data['oil']) + sum(data['tires']) - 5
        return render(request, 'tickets/service.html', context={'number': number, 'minutes': min_to_wait})


class ServiceViewDiagnostic(View):
    def get(self, request, *args, **kwargs):
        global ticket_number
        numbers[2].append(ticket_number)
        ticket_number += 1
        data['diagnostics'].append(30)
        number = len(data['diagnostics'])
        min_to_wait = sum(data['oil']) + sum(data['tires']) + sum(data['diagnostics']) - 30
        return render(request, 'tickets/service.html', context={'number': number, 'minutes': min_to_wait})


class OperatorMenuView(RedirectView):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/operator_menu.html', context={'oil_queue': len(data['oil']), 'tires_queue': len(data['tires']), 'diagnostic_queue': len(data['diagnostics']) })

    def post(self, request, *args, **kwargs):
        global clicked
        global ticket_number
        global result_num
        if data['oil']:
            result_num = numbers[0].popleft()
            del data['oil'][0]
            clicked = True
            return redirect('/next')
        elif data['tires']:
            result_num = numbers[1].popleft()
            del data['tires'][0]
            clicked = True
            return redirect('/next')
        elif data['diagnostics']:
            result_num = numbers[2].popleft()
            del data['diagnostics'][0]
            clicked = True
            return redirect('/next')
        else:
            ticket_number = 1
            return redirect('/next')


class NextTicketView(RedirectView):
    def get(self, request, *args, **kwargs):
        if clicked:
            return render(request, 'tickets/next.html', context={'num': result_num})
        else:
            return render(request, 'tickets/next.html')


