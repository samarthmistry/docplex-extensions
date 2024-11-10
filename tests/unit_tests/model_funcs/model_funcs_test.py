# Copyright 2024 Samarth Mistry
# This file is part of the `docplex-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""Model functionality."""

import pytest
from docplex.mp.model import Model

from docplex_extensions import print_problem_stats, print_solution_quality_stats, solve

from .conftest import regex_trim


def validate_logoutput(input, expected_log_start, expected_log_end):
    input_pre = input.split('CPLEX optimizer log')[0]
    expected_pre = expected_log_start.split('CPLEX optimizer log')[0]

    input_post = input.split('Solution quality statistics')[1]
    expected_post = expected_log_end.split('Solution quality statistics')[1]

    assert regex_trim(input_pre) == regex_trim(expected_pre)
    assert regex_trim(input_post) == regex_trim(expected_post)


def test_print_model_stats_pass(capsys, mdl):
    print_problem_stats(mdl)

    captured = capsys.readouterr().out
    expected = '\n'.join(
        [
            f'Problem name         : {mdl.name}',
            'Objective sense      : Minimize',
            'Variables            :       0',
            'Objective nonzeros   :       0',
            'Linear constraints   :       0',
            '  Nonzeros           :       0',
            '  RHS nonzeros       :       0',
            '',
            'Variables            : Min LB: all infinite     Max UB: all infinite   ',
            'Objective nonzeros   : Min   : all zero         Max   : all zero       ',
            'Linear constraints   :',
            '  Nonzeros           : Min   : all zero         Max   : all zero       ',
            '  RHS nonzeros       : Min   : all zero         Max   : all zero       ',
            '',
            '',
        ]
    )

    assert regex_trim(captured) == regex_trim(expected)


def test_print_solution_quality_stats_unsolved_pass(capsys, mdl):
    print_solution_quality_stats(mdl)

    captured = capsys.readouterr().out
    expected = f'Model `{mdl.name}` has no incumbent solution.\n'

    assert regex_trim(captured) == regex_trim(expected)


def test_print_solution_quality_stats_solved_pass(capsys, mdl):
    _ = mdl.solve()
    print_solution_quality_stats(mdl)

    captured = capsys.readouterr().out
    expected = '\n'.join(
        [
            'There are no bound infeasibilities.',
            'There are no reduced-cost infeasibilities.',
            'Maximum Ax-b residual              = 0',
            "Maximum c-B'pi residual            = 0",
            'Maximum |x|                        = 0',
            'Maximum |pi|                       = 0',
            'Maximum |red-cost|                 = 0',
            'Condition number of unscaled basis = 0.0e+00',
            '',
            '',
        ]
    )

    assert regex_trim(captured) == regex_trim(expected)


def test_solve_solution_pass():
    mdl = Model(name='telephone_production')
    desk = mdl.continuous_var(name='desk')
    cell = mdl.continuous_var(name='cell')
    mdl.add_constraint_(desk >= 100)
    mdl.add_constraint_(cell >= 100)
    mdl.add_constraint_(0.2 * desk + 0.4 * cell <= 400)
    mdl.add_constraint_(0.5 * desk + 0.4 * cell <= 490)
    mdl.maximize(12 * desk + 20 * cell)

    sol1 = mdl.solve()
    sol2 = solve(mdl, clean_before_solve=True)

    assert sol1.to_string() == sol2.to_string()


def test_solve_logoutput_true_pass(capsys, mdl, expected_log_start, expected_log_end):
    _ = solve(mdl, log_output=True)
    captured = capsys.readouterr().out

    validate_logoutput(captured, expected_log_start % mdl.name, expected_log_end)


def test_solve_logoutput_context_pass(capsys, mdl, expected_log_start, expected_log_end):
    mdl.context.solver.log_output = True
    _ = solve(mdl)
    captured = capsys.readouterr().out

    validate_logoutput(captured, expected_log_start % mdl.name, expected_log_end)


def test_solve_logoutput_stdout_pass(capsys, mdl, expected_log_start, expected_log_end):
    _ = solve(mdl, log_output='stdout')
    captured = capsys.readouterr().out

    validate_logoutput(captured, expected_log_start % mdl.name, expected_log_end)


def test_solve_logoutput_stderr_pass(capsys, mdl, expected_log_start, expected_log_end):
    _ = solve(mdl, log_output='stderr')
    captured = capsys.readouterr().err

    validate_logoutput(captured, expected_log_start % mdl.name, expected_log_end)


def test_solve_logoutput_file_pass(tmpdir, mdl, expected_log_start, expected_log_end):
    file = tmpdir.join('file.log')
    _ = solve(mdl, log_output=file.strpath)
    captured = file.read()

    validate_logoutput(captured, expected_log_start % mdl.name, expected_log_end)


@pytest.mark.parametrize('config', ['log_output=False', 'no log_output'])
def test_solve_logoutput_false_pass(capsys, mdl, config):
    if config == 'log_output=False':
        _ = solve(mdl, log_output=False)
    if config == 'no log_output':
        _ = solve(mdl)

    captured = capsys.readouterr()
    expected = ''

    assert captured.out == expected


@pytest.mark.parametrize('mdl', ['abc', 123, ('A', 'B')])
def test_solve_mdl_typerr(mdl):
    with pytest.raises(TypeError):
        solve(mdl)
