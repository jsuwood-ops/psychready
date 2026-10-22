const b=document.querySelector('.menu-btn'),n=document.getElementById('nav');b&&b.addEventListener('click',()=>{const o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
document.querySelectorAll('[data-print]').forEach(el=>el.addEventListener('click',()=>print()));
const thanks=document.getElementById('seat-thanks');
if(thanks&&new URLSearchParams(location.search).get('seats')==='success')thanks.hidden=false;
