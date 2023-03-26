def make_short_search_query_params(
    cal_input_text_from: str,
    cal_input_text_to: str,
    classic_cargo: bool,
    truck_select: list[str],
    multisearch_block_from: list[list[str]],
    multisearch_block_to: list[list[str]],
    is_not_deleted_filter: bool,
    is_customer_filter: bool,
    is_partner_filter: bool,
    is_not_black_filter: bool,
    is_load_up_filter: bool,
    is_adr_filter: bool,
    is_trans_with_gps_filter: bool,
    is_humanitarian_filter: bool,
    is_only_new_filter: bool,
    is_only_from_verified_filter: bool,
    group_filter_select: str,
    price_type_filter: list[str],
    search_time_filter_select: str,
    load_type_filter: list[str],
    bookmark_number: str,
    weight_from: str = '0',
    weight_to: str = '0',
    cube_from: str = '0',
    cube_to: str = '0',
) -> str:
    location = ''
    truck_array = []
    date_from = (
        cal_input_text_from.replace('/', '-') if cal_input_text_from else '0'
    )
    date_to = cal_input_text_to.replace('/', '-') if cal_input_text_to else '0'
    cargo = 'cargo' if classic_cargo else 'trans'
    citid = (
        cf_array
    ) = rf_array = cif_array = ct_array = rt_array = cit_array = []
    False

    for truck_id in truck_select:
        if truck_id != '6' and truck_id not in truck_array:
            truck_array.append(truck_id)

    for multisearch_block in multisearch_block_from:
        if len(cf_array) < 8:
            cid = multisearch_block[0]
            rid = multisearch_block[1]
            citid = multisearch_block[2]
            if cid == '0' or (
                len(cf_array) > 0
                and cf_array[-1] == cid
                and rf_array[-1] == rid
                and cif_array[-1] == citid
            ):
                continue
            cf_array.append(cid)
            rf_array.append(rid)
            cif_array.append(citid)
            if citid != '0':
                pass

    for multisearch_block in multisearch_block_to:
        if len(ct_array) < 8:
            cid = multisearch_block[0]
            rid = multisearch_block[1]
            citid = multisearch_block[2]
            if cid == '0' or (
                len(ct_array) > 0
                and ct_array[-1] == cid
                and rt_array[-1] == rid
                and cit_array[-1] == citid
            ):
                continue
            ct_array.append(cid)
            rt_array.append(rid)
            cit_array.append(citid)
            if citid != '0':
                pass

    if not cf_array and not ct_array:
        raise ValueError('No search location provided')

    location += f'a{"l".join(cf_array)}b{"l".join(rf_array)}'
    if cif_array:
        location += f'j{"l".join(cif_array)}'
    location += f'd{"l".join(ct_array)}e{"l".join(rt_array)}'
    if cit_array:
        location += f't{"l".join(cit_array)}'
    location += 'f'

    if cube_from != '0' or cube_to != '0':
        if cube_from != '0':
            location += cube_from
        location += 'l'
        if cube_to != '0':
            location += cube_to
    location += 'o'

    if weight_from != '0' or weight_to != '0':
        if weight_from != '0':
            location += weight_from
        location += 'l'
        if weight_to != '0':
            location += weight_to

    filters = [
        {'mask': 'z1', 'condition': is_not_deleted_filter},
        {'mask': 'z2', 'condition': is_customer_filter and cargo == 'cargo'},
        {'mask': 'z3', 'condition': is_partner_filter},
        {'mask': 'z4', 'condition': is_not_black_filter},
        {'mask': 'z9', 'condition': is_load_up_filter},
        {'mask': 'y1', 'condition': is_adr_filter},
        {
            'mask': 'y3',
            'condition': is_trans_with_gps_filter and cargo == 'trans',
        },
        {'mask': 'y4', 'condition': is_humanitarian_filter},
        {'mask': 'z7', 'condition': is_only_new_filter},
        {'mask': 'y5', 'condition': is_only_from_verified_filter},
        {'mask': 'y6', 'value': int(group_filter_select)},
        {'mask': 'z5', 'value': sum(map(int, price_type_filter))},
        {'mask': 'z6', 'value': int(search_time_filter_select)},
        {'mask': 'y2', 'value': sum(map(int, load_type_filter))},
    ]

    for filt in filters:
        if filt.get('condition'):
            location += f'{filt["mask"]}{filt.get("value", 1)}'

    location += f'h{"l".join(truck_array)}'

    if date_from != '0' or date_to != '0':
        timeNow = datetime.now()
        time_from = datetime.strptime(date_from, '%Y-%m-%d')
        time_to = datetime.strptime(date_to, '%Y-%m-%d')

        is_add_date_params = True
        if (
            timeNow.day == time_from.day
            and timeNow.month == time_from.month
            and timeNow.year == time_from.year
            and (
                (
                    timeNow.day == time_to.day
                    and time_to.month - timeNow.month == 2
                    and timeNow.year == time_to.year
                )
                or (
                    timeNow.day == time_to.day
                    and time_to.month + 12 - timeNow.month == 2
                    and timeNow.year == time_to.year - 1
                )
            )
        ):
            is_add_date_params = False

        if is_add_date_params:
            location += f'{date_from}l{date_to}'
        else:
            location += 'l'

    location += f'k{int(cargo == "trans")}'
    location += f'm{bookmark_number}' if bookmark_number else ''

    return location


def make_short_search_query_url() -> str:
    params = make_short_search_query_params(
        ...
    )  # pass in all the required arguments
    return f'//{DELLA_URL}{ADD_PATH}/search/{params}.html' if params else ''
