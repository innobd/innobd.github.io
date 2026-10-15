(function () {
  var root = document.documentElement;
  var saved = null;
  try { saved = localStorage.getItem('innobd-lang'); } catch (e) {}
  var lang = (saved === 'en' || saved === 'ko') ? saved : 'ko';
  function apply(l) {
    lang = l;
    root.setAttribute('data-lang', l);
    try { localStorage.setItem('innobd-lang', l); } catch (e) {}
    var btns = document.querySelectorAll('.lang button');
    for (var i = 0; i < btns.length; i++) {
      btns[i].setAttribute('aria-pressed', btns[i].getAttribute('data-lang') === l ? 'true' : 'false');
    }
  }
  apply(lang);
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest && ev.target.closest('.lang button');
    if (b) apply(b.getAttribute('data-lang'));
  });
})();
