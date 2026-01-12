import logging
import time

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect

from apps.core.helpers.sudoku_helper import *

logger = logging.getLogger(__name__)

@require_http_methods(["GET"])
def home(request: HttpRequest) -> HttpResponse:
    context = {'matrix': [[0]*9 for _ in range(9)], 'introduced_values': []}
    return render(request, "core/home.html", context)

@csrf_protect
@require_http_methods(["GET", "POST"])
def action_form(request: HttpRequest) -> HttpResponse:
    time0 = time.time()
    context = {'error': None, 'matrix': [[0]*9 for _ in range(9)], 'introduced_values': []}
    if request.method == "POST": #~ When is POST.
        matrix = [[0]*9 for _ in range(9)]
        introduced_values = []
        #~ Verify if all the cells are numeric and between 1 and 9.
        error = validate_the_numerical_values_and_fill_the_matrix(matrix, introduced_values, request.POST)
        if error is None:
            #~ Verify if the Sudoku table is well-structured and all the cells can have one or more posible values.
            if is_valid_sudoku(matrix):
                #~ Solving the Sudoku table.
                solve_sudoku(matrix)
                logger.info("Time of solution: %.3f secs.", time.time() - time0)
            else:
                error = "The sudoku is invalid."
                introduced_values = []
        context = {'error': error, 'matrix': matrix, 'introduced_values': introduced_values}
    return render(request, "core/home.html", context)