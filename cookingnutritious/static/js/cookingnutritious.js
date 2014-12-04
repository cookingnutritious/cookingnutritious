function nutrient_map() {
    this.total_fat = 'Total lipid (fat)';
    this.saturated_fat = 'Fatty acids, total saturated';
    this.trans_fat = 'Fatty acids, total trans';
    this.cholesterol = 'Cholesterol';
    this.sodium = 'Sodium, Na';
    this.carbohydrate = 'Carbohydrate, by difference';
    this.fiber = 'Fiber, total dietary';
    this.sugars = 'Sugars, total';
    this.protein = 'Protein';
    this.vitamin_a = 'Vitamin A, IU';
    this.vitamin_b = 'Vitamin B-12';
    this.vitamin_c = 'Vitamin C, total ascorbic acid';
    this.vitamin_d = 'Vitamin D (D2 + D3)';
    this.calcium = 'Calcium, Ca';
    this.iron = 'Iron, Fe';
    this.potassium = 'Potassium, K';
}

function get_nutrients(data) {
    result = {}
    for (var item in data) {
        for (var key in data[item]) {
            result[key] = data[item][key];
        }
    }
    return result;
}


function cn_clean_search_term(srch_val) {
    srch_val = encodeURIComponent(srch_val);
    srch_val = srch_val.replace(/%20/g, '_');
    srch_val = srch_val.replace(/%2C/g, '');
    srch_val = srch_val.replace(/\'/g, 'XX');
    srch_val = srch_val.replace(/\./g, 'QQ');
    srch_val = srch_val.replace(/%22/g, 'YY');
    srch_val = srch_val.replace(/"/g, 'YY');
    srch_val = srch_val.replace(/%2F/g, 'ZZ');
    srch_val = srch_val.replace(/%25/g, '');
    srch_val = srch_val.replace(/\(/g, '_');
    srch_val = srch_val.replace(/\)/g, '_');
    return srch_val
}

function get_total_calories(protein, fat, carb) {
    var kcal_protein = protein * 4;
    var kcal_carb = carb * 4;
    var kcal_fat = fat * 9;
    return (kcal_protein + kcal_carb + kcal_fat);
}

function nutritious_info(data, grams) {
    var normalizer = grams / 100;
    var map = new nutrient_map();
    var item = data[0];
    for (var key in map) {
        this[key] = (data[map[key]]) * normalizer;
    }
    this.calories = get_total_calories(this.protein, this.total_fat, this.carbohydrate);

}

function get_nutrition_data(url) {
    $.getJSON(url)
        .done(function (data) {
            if (data.length > 1) {
                get_nutrition_data(data[0].url);
            } else {
                if (typeof data == 'object') {
                    if (data.length > 0) {
                        var item = data[0];
                    } else {
                        var item = data;
                    }

                    var measurement = measurements[$('#id_measurement option:selected').text()];
                    console.log(measurement);
                    if (measurement == "" || measurement == undefined) {
                        measurement = 100;
                    }
                    
                    var nutritents = get_nutrients(item.nutrients);
                    var nutrition = new nutritious_info(nutritents, measurement);
                    for (var i in nutrition) {
                        var value = Math.round(nutrition[i] * 100) / 100;
                        if (isNaN(value)) { value = 0 }
                        $('#id_' + i).val(value);
                    }
                } else {
                    return false;
                }
            }
        })
}

var measurements = {};

$(document).ready(function () {
    var measurements_endpoint = $('#id_measurement').attr("data-measurement-endpoint");

    $.getJSON(measurements_endpoint)
            .done(function (data) {
                if (typeof data == 'object') {
                    for (var i in data) {
                        measurements[data[i]['unit']] = data[i]['gram_weight'];
                    }
                } else {
                    return false;
                }
            });

    $('#id_long_description_btn').click(function() {
        var srch_val = cn_clean_search_term($('#id_long_description').val());
        var url_template = $('#id_long_description_btn').attr("data-url-template");
        var url = url_template.replace("__long_description__", srch_val);
        window.location = url
        return false;
    });

    $('#id_name').bind('selectChoice', function (e, choice, autocomplete) {
        var srch_val = cn_clean_search_term(choice.text());
        var url_template = $('#id_name').attr("data-url-template");
        var url = url_template.replace("__long_description__", srch_val);
        get_nutrition_data(url);
        return false;
    });

    $('#id_measurement').change(function () {
        var srch_val = cn_clean_search_term($('#id_name').val());
        var url_template = $('#id_name').attr("data-url-template");
        var url = url_template.replace("__long_description__", srch_val);
        var measurement = measurements[$('#id_measurement option:selected').text()];
        get_nutrition_data(url);
        return false;
    });


});
