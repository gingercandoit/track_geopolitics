/* ================================================================
   Geopolitical Economics Monthly — Client JS
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
          detail.style.maxHeight = (detail.scrollHeight + 40) + 'px';
        }
      }
      return;
    }
  });

  /* ── Month persistence across topic navigation ───────────── */
  var MONTH_KEY = 'gem_selected_month';

  // Detect current month from URL: e.g. /topic1-sanctions/2026-03.html → "2026-03"
  function detectCurrentMonth() {
    var path = window.location.pathname;
    var match = path.match(/\/topic\d+-[^\/]+\/(\d{4}-\d{2})\.html/);
    return match ? match[1] : null;
  }

  // Rewrite all topic nav links to use the stored month
  function rewriteTopicLinks(month) {
    if (!month) return;
    document.querySelectorAll('.nav-link').forEach(function (a) {
      var href = a.getAttribute('href');
      if (!href) return;
      // Only rewrite topic links (pattern: .../topicN-slug/YYYY-MM.html)
      var replaced = href.replace(
        /(\/topic\d+-[^\/]+\/)\d{4}-\d{2}(\.html)/,
        '$1' + month + '$2'
      );
      if (replaced !== href) {
        a.setAttribute('href', replaced);
      }
    });
  }

  // On page load: persist current month and rewrite links
  var currentMonth = detectCurrentMonth();
  if (currentMonth) {
    try { localStorage.setItem(MONTH_KEY, currentMonth); } catch (e) {}
  }
  var storedMonth = null;
  try { storedMonth = localStorage.getItem(MONTH_KEY); } catch (e) {}
  if (storedMonth) {
    rewriteTopicLinks(storedMonth);
    // Also update the nav month selector dropdown to match stored month
    var navSelect = document.querySelector('.nav-issue-select');
    if (navSelect && !currentMonth) {
      // On non-topic pages, don't force-select — leave as-is
    } else if (navSelect) {
      // On topic pages, selector is already correct from Jinja2
    }
  }

  /* ── Month navigation ───────────────────────────────────────── */
  window.navigateMonth = function (url) {
    if (url) {
      // Extract month from the target URL and persist
      var match = url.match(/(\d{4}-\d{2})\.html/);
      if (match) {
        try { localStorage.setItem(MONTH_KEY, match[1]); } catch (e) {}
      }
      window.location.href = url;
    }
  };

  /* ── Overview toggle (global function for inline onclick) ──── */
  window.toggleOverview = function () {
    var el = document.getElementById('overviewText');
    var btn = document.getElementById('overviewToggle');
    if (!el || !btn) return;
    var isCollapsed = el.classList.contains('collapsed');
    el.classList.toggle('collapsed');
    btn.textContent = isCollapsed ? '收起 ▴' : '展开全文 ▾';
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

  /* ── Overview collapse (auto-collapse if content is tall) ──── */
  var overviewEl = document.getElementById('overviewText');
  var overviewBtn = document.getElementById('overviewToggle');
  if (overviewEl && overviewBtn) {
    // If content fits in 12em (~200px), hide the button
    var threshold = 200;
    if (overviewEl.scrollHeight > threshold) {
      overviewEl.classList.add('collapsed');
    } else {
      overviewBtn.classList.add('hidden');
    }
  }

})();
