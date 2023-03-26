// Code from della.kz

function make_short_search_query_params() {
    var location = '',
    truck_array = [
    ],
    weightFrom = document.getElementById('SelectWeightFrom') && document.getElementById('SelectWeightFrom').value || 0,
    weightTo = document.getElementById('SelectWeightTo') && document.getElementById('SelectWeightTo').value || 0,
    cubeFrom = document.getElementById('SelectCubeFrom') && document.getElementById('SelectCubeFrom').value || 0,
    cubeTo = document.getElementById('SelectCubeTo') && document.getElementById('SelectCubeTo').value || 0,
    date_from = document.getElementById('calInputTextFrom') && document.getElementById('calInputTextFrom').getAttribute('datevalue').replace(/\//g, '-') || 0,
    date_to = document.getElementById('calInputTextTo') && document.getElementById('calInputTextTo').getAttribute('datevalue').replace(/\//g, '-') || 0,
    cargo = document.getElementById('classicCargo_').checked ? 'cargo' : 'trans',
    cid = !1,
    rid = !1,
    citid = !1,
    cf_array = [
    ],
    rf_array = [
    ],
    cif_array = [
    ],
    ct_array = [
    ],
    rt_array = [
    ],
    cit_array = [
    ],
    got_cities_from = !1,
    got_cities_to = !1;
    if ($('.multiTruckBlock .truck_select').each((function () {
        for (var truck_id = 6 != $(this).val() && $(this).val() || 0, unique = !0, i = 0; i < truck_array.length; i++) if (truck_array[i] == truck_id) {
            unique = !1;
            break
        }
        unique && truck_array.push(truck_id)
    })), $('#marshrutteKeeperFrom table.multisearchBlock').each((function () {
        cf_array.length < 8 && (cid = $(this).find('.country_select').val(), rid = $(this).find('.region_select').val(), citid = $(this).find('.city_input').attr('data-city-uid'), '0' == cid || cf_array.slice( - 1) [0] == cid && rf_array.slice( - 1) [0] == rid && cif_array.slice( - 1) [0] == citid || (cf_array.push(cid), rf_array.push(rid), cif_array.push(citid), 0 != citid && (got_cities_from = !0)))
    })), $('#marshrutteKeeperTo table.multisearchBlock').each((function () {
        ct_array.length < 8 && (cid = $(this).find('.country_select').val(), rid = $(this).find('.region_select').val(), citid = $(this).find('.city_input').attr('data-city-uid'), '0' == cid || ct_array.slice( - 1) [0] == cid && rt_array.slice( - 1) [0] == rid && cit_array.slice( - 1) [0] == citid || (ct_array.push(cid), rt_array.push(rid), cit_array.push(citid), 0 != citid && (got_cities_to = !0)))
    })), 1 == rf_array.length && '0' == rf_array[0] && (rf_array = [
    ]), 1 == rt_array.length && '0' == rt_array[0] && (rt_array = [
    ]), got_cities_from || (cif_array = [
    ]), got_cities_to || (cit_array = [
    ]), !cf_array.length && !ct_array.length) return alert(g_phrase[1030]),
    !1;
    if ($('#search_request_button').css('color', 'red'), $('#t44k').css('color', 'red'), location += 'a' + cf_array.join('l') + 'b' + rf_array.join('l') + (cif_array.length ? 'j' + cif_array.join('l') : '') + 'd' + ct_array.join('l') + 'e' + rt_array.join('l') + (cit_array.length ? 't' + cit_array.join('l') : ''), location += 'f', 0 === cubeFrom && 0 === cubeTo || (0 != cubeFrom && (location += cubeFrom), location += 'l', 0 != cubeTo && (location += cubeTo)), location += 'o', 0 === weightFrom && 0 === weightTo || (0 != weightFrom && (location += weightFrom), location += 'l', 0 != weightTo && (location += weightTo)), [
        {
            mask: 'z1',
            selector: '.isNotDeleted_filter'
        },
        {
            mask: 'z2',
            selector: '.isCustomer_filter',
            additionalCondition: function ($filterContainer) {
                return 'cargo' === cargo
            }
        },
        {
            mask: 'z3',
            selector: '.isPartner_filter'
        },
        {
            mask: 'z4',
            selector: '.isNotBlack_filter'
        },
        {
            mask: 'z9',
            selector: '.isLoadUp_filter'
        },
        {
            mask: 'y1',
            selector: '.isADR_filter'
        },
        {
            mask: 'y3',
            selector: '.isTransWithGPS_filter',
            additionalCondition: function ($filterContainer) {
                return 'trans' === cargo
            }
        },
        {
            mask: 'y4',
            selector: '.isHumanitarian_filter'
        },
        {
            mask: 'z7',
            selector: '.isOnlyNew_filter'
        },
        {
            mask: 'y5',
            selector: '.isOnlyFromVerified_filter'
        },
        {
            mask: 'y6',
            selector: '.groupFilter_filter',
            generateValue: $filterContainer=>{
                let value = Number($filterContainer.find('#group_filter_select option:selected').val());
                return isNaN(value) ? 0 : value
            }
        },
        {
            mask: 'z5',
            selector: '.priceType_filter',
            generateValue: $filterContainer=>{
                let value = 0;
                return $filterContainer.find('.filter_checkbox_tag.checked').each((function () {
                    let tagMask = $(this).attr('data-tag-mask');
                    value |= tagMask
                })),
                value
            }
        },
        {
            mask: 'z6',
            selector: '#search_time_filter_select',
            generateValue: $filterContainer=>{
                let value = Number($filterContainer.find('option:selected').attr('data-time-mask'));
                return isNaN(value) ? 0 : value
            }
        },
        {
            mask: 'y2',
            selector: '.loadType_filter',
            generateValue: $filterContainer=>{
                let value = 0;
                return $filterContainer.find('.filter_checkbox_tag.checked').each((function () {
                    let tagMask = $(this).attr('data-tag-mask');
                    value |= tagMask
                })),
                value
            }
        }
    ].forEach((function (filter) {
        let value,
        $filterContainer = $(filter.selector);
        value = 'function' == typeof filter.generateValue ? filter.generateValue($filterContainer) : Number($filterContainer.find('.filter_checkbox').hasClass('checked'));
        let additionalCondition = !0;
        'function' == typeof filter.additionalCondition && (additionalCondition = filter.additionalCondition($filterContainer)),
        0 !== value && additionalCondition && (location += filter.mask + value)
    })), location += 'h' + truck_array.join('l'), location += 'i', 0 !== date_from || 0 !== date_to) {
        var timeNow = new Date,
        timeFrom = getDateObject(date_from),
        timeTo = getDateObject(date_to),
        is_add_date_params = !0;
        timeNow.getDate() == timeFrom.getDate() && timeNow.getMonth() == timeFrom.getMonth() && timeNow.getYear() == timeFrom.getYear() && (timeNow.getDate() == timeTo.getDate() && timeTo.getMonth() - timeNow.getMonth() == 2 && timeNow.getYear() == timeTo.getYear() || timeNow.getDate() == timeTo.getDate() && timeTo.getMonth() + 12 - timeNow.getMonth() == 2 && timeNow.getYear() == timeTo.getYear() - 1) && (is_add_date_params = !1),
        location += is_add_date_params ? convertDate(date_from) + 'l' + convertDate(date_to) : 'l'
    }
    return location += 'k' + ('trans' == cargo ? 1 : 0),
    location += 'm' + (document.getElementById('bookmark_number') ? document.getElementById('bookmark_number').value : '')
}
function make_short_search_query_url() {
    var params = make_short_search_query_params();
    return !!params && '//' + DELLA_URL + ADD_PATH + '/search/' + params + '.html'
}