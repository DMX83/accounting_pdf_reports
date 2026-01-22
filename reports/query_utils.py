# -*- coding: utf-8 -*-

def query_get(aml, domain=None):
    domain = list(domain or [])
    ctx = aml.env.context

    def _normalize_id(value):
        if isinstance(value, (list, tuple)):
            if value and isinstance(value[0], (list, tuple)):
                return [v[0] for v in value]
            if len(value) == 2 and isinstance(value[0], int):
                return value[0]
        return value

    journal_ids = _normalize_id(ctx.get('journal_ids'))
    if journal_ids:
        domain.append(('journal_id', 'in', journal_ids))
    if ctx.get('state') == 'posted':
        domain.append(('move_id.state', '=', 'posted'))
    if ctx.get('date_from'):
        if ctx.get('initial_bal'):
            domain.append(('date', '<', ctx['date_from']))
        else:
            domain.append(('date', '>=', ctx['date_from']))
    if ctx.get('date_to'):
        domain.append(('date', '<=', ctx['date_to']))
    company_id = _normalize_id(ctx.get('company_id'))
    if company_id:
        if isinstance(company_id, (list, tuple)):
            domain.append(('company_id', 'in', company_id))
        else:
            domain.append(('company_id', '=', company_id))
    elif ctx.get('allowed_company_ids'):
        domain.append(('company_id', 'in', ctx['allowed_company_ids']))

    query = aml._where_calc(domain)
    aml._apply_ir_rules(query, 'read')

    from_clause = query.from_clause._SQL__code
    where_clause = query.where_clause._SQL__code or "TRUE"
    where_params = list(query.from_clause._SQL__params) + list(query.where_clause._SQL__params)
    return from_clause, where_clause, where_params
