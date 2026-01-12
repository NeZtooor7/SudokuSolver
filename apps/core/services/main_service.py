import logging
import time

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect

from apps.core.helpers.sudoku_helper import *

DIMENSION_OF_SUDOKU_TABLE = 9
LOGGER = logging.getLogger(__name__)

@require_http_methods(["GET"])
def home(request: HttpRequest) -> HttpResponse:
    matrix = [[0] * DIMENSION_OF_SUDOKU_TABLE for _ in range(DIMENSION_OF_SUDOKU_TABLE)]
    context = {'matrix': matrix, 'introduced_values': []}
    return render(request, "core/home.html", context)

@csrf_protect
@require_http_methods(["GET", "POST"])
def action_form(request: HttpRequest) -> HttpResponse:
    time0 = time.time()
    matrix = [[0] * DIMENSION_OF_SUDOKU_TABLE for _ in range(DIMENSION_OF_SUDOKU_TABLE)]
    context = {'error': None, 'matrix': matrix, 'introduced_values': []}
    if request.method == "POST": #~ When is POST.
        introduced_values = []
        #~ Verify if all the cells are numeric and between 1 and 9.
        error = validate_the_numerical_values_and_fill_the_matrix(matrix, introduced_values, request.POST)
        if error is None:
            #~ Verify if the Sudoku table is well-structured and all the cells can have one or more posible values.
            if is_valid_sudoku(matrix):
                #~ Solving the Sudoku table.
                solve_sudoku(matrix)
                LOGGER.info("Time of solution: %.3f secs.", time.time() - time0)
            else:
                error = "The sudoku is invalid."
                introduced_values = []
        context = {'error': error, 'matrix': matrix, 'introduced_values': introduced_values}
    return render(request, "core/home.html", context)