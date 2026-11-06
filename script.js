// Menu mobile
const toggle = document.querySelector('.nav-toggle');
const nav = document.getElementById('menu');
toggle.addEventListener('click', () => {
  const open = nav.classList.toggle('is-open');
  toggle.setAttribute('aria-expanded', open);
  toggle.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
});
nav.addEventListener('click', (e) => {
  if (e.target.closest('a')) { nav.classList.remove('is-open'); toggle.setAttribute('aria-expanded', 'false'); }
});

// Animações ao rolar (sem suporte: mostra tudo direto)
const reveals = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('is-visible'); io.unobserve(en.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  reveals.forEach((el) => io.observe(el));
} else {
  reveals.forEach((el) => el.classList.add('is-visible'));
}

// Lightbox da galeria
const items = [...document.querySelectorAll('.gallery__item')];
const box = document.querySelector('.lightbox');
const boxImg = box.querySelector('img');
let current = 0;
const show = (i) => {
  current = (i + items.length) % items.length;
  const img = items[current].querySelector('img');
  boxImg.src = items[current].dataset.full;
  boxImg.alt = img.alt;
};
items.forEach((btn, i) => {
  btn.setAttribute('aria-label', 'Ampliar foto: ' + btn.querySelector('img').alt);
  btn.addEventListener('click', () => { show(i); box.showModal(); });
});
box.querySelector('.lightbox__close').addEventListener('click', () => box.close());
box.querySelector('.lightbox__prev').addEventListener('click', () => show(current - 1));
box.querySelector('.lightbox__next').addEventListener('click', () => show(current + 1));
box.addEventListener('click', (e) => { if (e.target === box) box.close(); }); // clique no fundo fecha
box.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowLeft') show(current - 1);
  if (e.key === 'ArrowRight') show(current + 1);
});
box.addEventListener('close', () => items[current].focus());

document.getElementById('ano').textContent = new Date().getFullYear();
