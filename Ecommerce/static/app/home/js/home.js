$(
    function () {
        //chu shi hua
        initTopWheel();
        initTopWheel2();
    }
);


function initTopWheel() {
    var mySwiper = new Swiper('#topSwiper',{
pagination : '.swiper-pagination',
	autoplay: 3000,//可选选项，自动滑动
})

}

function initTopWheel2() {
    var swiper = new Swiper('#swiperMenu', {
        slidesPerView: 3,


      });

}



