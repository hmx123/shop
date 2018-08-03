$(function () {
    $('#show1').click(
        function () {
            //dian ji quan bu lei xing de shi hou cheng xian
            $('#typeshow').show();
            $('#sort_list').hide();

            //dian ji lei xing lie biao shi hou guna bi
            $('#all_type_icon1').attr('class', 'glyphicon glyphicon-chevron-down')

            //dian ji lei xing lie biao shi hou guna bi
            $('#all_type_icon').attr('class', 'glyphicon glyphicon-chevron-up')

        }

    );
    $('#typeshow').click(
        function(){
            $('#typeshow').hide();
            $('#all_type_icon').attr('class', 'glyphicon glyphicon-chevron-down')
        }

    );
    //dian ji zhong he pai xu xian shi pai xu lie biao
    $('#all_sort').click(
        function () {
            //dian ji quan bu lei xing de shi hou cheng xian
            $('#sort_list').show();
            $('#typeshow').hide();
            $('#all_type_icon').attr('class', 'glyphicon glyphicon-chevron-down')

            //dian ji lei xing lie biao shi hou guna bi
            $('#all_type_icon1').attr('class', 'glyphicon glyphicon-chevron-up')

        }

    );

    $('#sort_list').click(
        function () {
            //dian ji quan bu lei xing de shi hou cheng xian
            $('#sort_list').hide();

            //dian ji lei xing lie biao shi hou guna bi
            $('#all_type_icon1').attr('class', 'glyphicon glyphicon-chevron-down')

        }

    );
        //tain jia shang pin shu liang
    $('.addCart').click(function () {

        var gid = $(this).attr('goodid')
        // console.log(gid)
        var addGoods = $(this)
        $.getJSON('/app/add_card_num/', {'gid':gid},function (data) {
            if (data.code == '700'){
                window.open('/app/login/', target='_self')
            }else if(data.code == '200'){
                addGoods.prev().html(data.cnum)
            }
        })
    })
    //jianshao shang pin shu liang
    $('.subCart').click(function () {
        var sid = $(this).attr('goodid')
        var subGoods = $(this)
        $.getJSON('/app/sub_card_num/', {'sid':sid},function (data) {
            if (data.code == '700'){
                window.open('/app/login/', target='_self')
            } else if (data.code == '703'){
                console.log('0')
            } else if (data.code == '200'){
                subGoods.next().html(data.cnum)
            }
        })

    })


});