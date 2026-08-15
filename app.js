
(function () {
  'use strict';

  var body = document.body;
  var toggle = document.getElementById('toggleTheme');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      body.setAttribute('data-theme', next);
      try { localStorage.setItem('woh-theme', next); } catch (e) {}
    });
  }

  var sets = Array.prototype.slice.call(document.querySelectorAll('.set'));
  if (!sets.length) return;

  var total = sets.length;
  var search = document.getElementById('search');
  var tally = document.getElementById('tally');
  var clearBtn = document.getElementById('clearFilters');
  var emptyMsg = document.getElementById('emptyMsg');
  var dayBtns = Array.prototype.slice.call(document.querySelectorAll('[data-day-filter]'));
  var catBtns = Array.prototype.slice.call(document.querySelectorAll('[data-filter]'));
  var stageBtns = Array.prototype.slice.call(document.querySelectorAll('[data-stage-filter]'));

  var activeDay = null;
  var activeCats = [];
  var activeStages = [];
  var term = '';

  function apply() {
    var visible = 0;
    sets.forEach(function (el) {
      var cats = el.getAttribute('data-cat').split('|');
      var dayOk = !activeDay || el.getAttribute('data-day') === activeDay;
      // Several sounds per set, so any selected sound matching is enough.
      var catOk = !activeCats.length || cats.some(function (c) { return activeCats.indexOf(c) !== -1; });
      var stageOk = !activeStages.length || activeStages.indexOf(el.getAttribute('data-stage')) !== -1;
      var nameOk = !term || el.getAttribute('data-name').indexOf(term) !== -1;
      var show = dayOk && catOk && stageOk && nameOk;
      el.hidden = !show;
      if (show) visible++;
    });

    var filtered = visible !== total;
    tally.textContent = filtered
      ? visible + ' of ' + total + ' sets'
      : total + ' sets';
    clearBtn.hidden = !filtered;
    emptyMsg.hidden = visible !== 0;
  }

  dayBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var d = btn.getAttribute('data-day-filter');
      var turningOff = activeDay === d;
      dayBtns.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
      activeDay = turningOff ? null : d;
      if (!turningOff) btn.setAttribute('aria-pressed', 'true');
      apply();
    });
  });

  catBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var f = btn.getAttribute('data-filter');
      var i = activeCats.indexOf(f);
      if (i !== -1) { activeCats.splice(i, 1); btn.setAttribute('aria-pressed', 'false'); }
      else { activeCats.push(f); btn.setAttribute('aria-pressed', 'true'); }
      apply();
    });
  });

  stageBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var s = btn.getAttribute('data-stage-filter');
      var i = activeStages.indexOf(s);
      if (i !== -1) { activeStages.splice(i, 1); btn.setAttribute('aria-pressed', 'false'); }
      else { activeStages.push(s); btn.setAttribute('aria-pressed', 'true'); }
      apply();
    });
  });

  search.addEventListener('input', function () {
    term = search.value.trim().toLowerCase();
    apply();
  });

  clearBtn.addEventListener('click', function () {
    activeDay = null;
    activeCats = [];
    activeStages = [];
    term = '';
    search.value = '';
    dayBtns.concat(catBtns, stageBtns).forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
    apply();
    search.focus();
  });

  // Names on the landing wall deep-link here as ?q=<artist>.
  var q = new URLSearchParams(window.location.search).get('q');
  if (q) {
    search.value = q;
    term = q.trim().toLowerCase();
  }

  apply();
})();
