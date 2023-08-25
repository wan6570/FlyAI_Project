searchform=document.querySelector('.header-1 .search-box');
document.querySelector('.icon .bx-search').onclick=()=>{
    searchform.classList.toggle('active'); 
}

window.onscroll=()=>{
    searchform.classList.remove('active'); 

    if (window.scrollY>80){
        document.querySelector('.header-1').classList.add('active');
    }else{
        document.querySelector('.header-1').classList.remove('active');
    } 
}

window.onload=()=>{
    if (window.scrollY>80){
        document.querySelector('.header-1').classList.add('active');
    }else{
        document.querySelector('.header-1').classList.remove('active');
    } 
}

/*var swiper =new Swiper(".gear",{
    loop:true,
    centeredSlides:true,
    autoplay:{
        delay:9500,
        disableOnInteraction:false,
},
breakpoints: {
    0:{
        slidesPerView:1,
    },
    768:{
        slidesPerView:2,
    },
    1024:{
        slidesPerView:3,
    },
},
});

var swiper =new Swiper(".slider",{
    spaceBetween:10,
    loop:true,
    centeredSlides:true,
    autoplay:{
        delay:9500,
        disableOnInteraction:false,
},
nevigation:{
    nextE1:".swiper-button-next",
    prevE1:".swiper-button-prev",
},
breakpoints: {
    0:{
        slidesPerView:1,
    },
    450:{
        slidesPerView:2,
    },
    768:{
        slidesPerView:3,
    },
    1024:{
        slidesPerView:4,
    },
},
});*/