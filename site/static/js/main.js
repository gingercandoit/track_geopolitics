/* ================================================================
   Geopolitical Research Quarterly — Client JS
   Card toggles, month navigation, mobile nav
   ================================================================ */

(function () {
  'use strict';

  /* ── Card expand / collapse ─────────────────────────────────── */
  document.addEventListener('click', function (e) {
    // Event cards (T1-T4)
    var header = e.target.closest('.event-card-header');
    if (header) {
      header.closest('.event-card').classList.toggle('expanded');
      return;
    }

    // Paper cards
    var paperHeader = e.target.closest('.paper-card-header');
    if (paperHeader) {
      paperHeader.closest('.paper-card').classList.toggle('expanded');
      return;
    }

    // T5 compact rows — toggle sibling detail
    var row = e.target.closest('.event-row');
    if (row) {
      var detail = row.nextElementSibling;
      if (detail && detail.classList.contains('event-row-detail')) {
        var isOpen = row.classList.contains('expanded');
        // close all other rows
        document.querySelectorAll('.event-row.expanded').forEach(function (r) {
          r.classList.remove('expanded');
        });
        document.querySelectorAll('.event-row-detail').forEach(function (d) {
          d.style.maxHeight = '0';
        });
        if (!isOpen) {
          row.classList.add('expanded');
          detail.style.maxHeight = detail.scrollHeight + 'px';
        }
      }
      return;
    }
  });

  /* ── Month navigation ───────────────────────────────────────── */
  window.navigateMonth = function (url) {
    if (url) {
      window.location.href = url;
    }
  };

  /* ── Mobile nav toggle ──────────────────────────────────────── */
  var toggle = document.querySelector('.nav-toggle');
  var links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      links.classList.toggle('open');
      var isOpen = links.classList.contains('open');
      toggle.textContent = isOpen ? '✕' : '☰';
      toggle.setAttribute('aria-expanded', isOpen);
    });
  }

})();
