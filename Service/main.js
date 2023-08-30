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