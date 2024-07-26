$(document).ready(function () {
    $('#id_region').change(function () {
        var regionId = $(this).val();
        if (regionId) {
            $.ajax({
                url: '{% url "obtener_comunas" %}',
                data: {
                    'region_id': regionId
                },
                dataType: 'json',
                success: function (data) {
                    $('#id_comuna').empty();
                    $.each(data, function (index, comuna) {
                        $('#id_comuna').append('<option value="' + comuna.id + '">' + comuna.nombre + '</option>');
                    });
                }
            });
        } else {
            $('#id_comuna').empty();
        }
    });

    // Cargar las comunas al cargar la página si la región ya está seleccionada
    var regionId = $('#id_region').val();
    if (regionId) {
        $.ajax({
            url: '{% url "obtener_comunas" %}',
            data: {
                'region_id': regionId
            },
            dataType: 'json',
            success: function (data) {
                $('#id_comuna').empty();
                $.each(data, function (index, comuna) {
                    $('#id_comuna').append('<option value="' + comuna.id + '">' + comuna.nombre + '</option>');
                });
            }
        });
    }
});