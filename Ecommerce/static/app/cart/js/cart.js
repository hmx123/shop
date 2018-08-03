// $(function () {
//     var select_on_off = $('#all_select_inner').attr('all_select_inner')
//     $('#all_select_inner').click(function () {
//         console.log('1111')
//         var is_choose = $('.is_choose')
//         // $('.is_choose').each(function () {
//             // is_choose.find('span').html('')
//             if(select_on_off == 'on'){
//                 $.getJSON('/app/allselected', {'status':'on'}, function (data) {
//                     var as = data['select']
//                     if (as == 'select') {
//
//                             $('.is_choose').each(function () {
//                               is_choose.find('span').html('')
//                         })
//
//                     }
//
//                 })
//                 select_on_off = 'off'
//             }else {
//              $.getJSON('/app/allselected/',{'status':'off'}, function (data) {
//                        var as = data['select'] //selected
//                         if( as == 'noselect'){
//                             $('.is_choose').each(function () {
//                                   is_choose.find('span').html('√')
//                             })
//                         }
//                 })
//                 select_on_off = 'on'
//             }
//         // })
//     })
//
//
// })


$(function () {

    var select_on_off = $('#all_select_inner').attr('all_select_inner')

//quna xuan huozhe bu xuan
    $('#all_select_inner').click(function () {
        // alert(12121)
        var is_choose = $('.is_choose')

        // $('.is_choose').each(function () {
        // is_choose.find('span').html('')
        if (select_on_off == 'on') {
            // 此时 是全部选中的状态 -- 》让其全不选中
            $.getJSON('/app/allselected/', {'status': 'on'}, function (data) {
                // console.log(data)
                var as = data['select'] //selected
                if (as == 'select') {
                    $('.is_choose').each(function () {
                        is_choose.find('span').html('')
                    })
                    $('#zhuang').html('')
                }
            })

            // 将标志设在为off
            select_on_off = 'off'
        } else {
            // 此时 是全不选中  ---》 全部选中
            $.getJSON('/app/allselected/', {'status': 'off'}, function (data) {
                var as = data['select'] //selected
                if (as == 'noselect') {
                    $('.is_choose').each(function () {
                        is_choose.find('span').html('√')
                    })
                    $('#zhuang').html('√')
                }
            })

            // 将标志设在为on
            select_on_off = 'on'
        }

        // })
    })

//dan xuan
    $('.is_choose').click(function () {
        var choose = $(this)
        var gid = choose.parents('li').attr('cartid')

        // console.log(gid)

        $.getJSON('/app/selectchange/', {'gid': gid}, function (data) {
            if (data.status) {
                choose.find('span').html('√')
            } else {
                choose.find('span').html('')
            }
            if (data.allselect) {
                $('#zhuang').html('√')
            } else {
                $('#zhuang').html('')
            }
        })
    })

    //zeng jia shang pin
    $('.addShopping').click(function () {
        var choose = $(this)
        var gid = choose.parents('li').attr('cartid')
        $.getJSON('/app/addshopping/', {'gid': gid}, function (data) {
            $.getJSON('/app/sumcart/', function (data) {
                $('#cartsum').html(data.cartsum)
            })

            choose.prev().html(data.cnum)
        })
    })
    //jian shao shang pin
    $('.subShopping').click(function () {
        var choose = $(this)
        var gid = choose.parents('li').attr('cartid')
        $.getJSON('/app/subshopping/', {'gid': gid}, function (data) {
            $.getJSON('/app/sumcart/', function (data) {
                $('#cartsum').html(data.cartsum)
            })
            console.log(data.cnum)
            if (data.cnum == 0) {
                choose.parents('li').remove()
            } else {
                choose.next().html(data.cnum)
            }

        })
    })
    //ji suan shang pin zhong jia


});

