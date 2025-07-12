// Code demo copy button logic for homepage
function copyDemoCode() {
  const code = document.getElementById('demo-code').innerText;
  navigator.clipboard.writeText(code);
  const btn = document.querySelector('.copy-btn');
  btn.innerHTML = '<i class="fas fa-check"></i>';
  setTimeout(() => { btn.innerHTML = '<i class="fas fa-copy"></i>'; }, 1500);
} 