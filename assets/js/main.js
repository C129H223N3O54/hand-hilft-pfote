/*
  Hand hilft Pfote – kleines Skript ohne externe Abhängigkeiten.
  - Mobiles Menü auf- und zuklappen
  - Großansicht für Galeriebilder
  Es werden keine Cookies, kein Browser-Speicher und keine Netzwerkanfragen an Dritte verwendet.
  Ohne JavaScript funktioniert die Seite weiterhin: Das Menü ist dann immer sichtbar,
  und Galeriebilder öffnen sich direkt als Datei.
*/
(function () {
  "use strict";
  document.documentElement.classList.add("js");

  /* ---------- Mobiles Menü ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("hauptmenue");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var offen = nav.classList.toggle("offen");
      toggle.setAttribute("aria-expanded", offen ? "true" : "false");
    });
  }

  /* ---------- Galerie-Großansicht ---------- */
  var links = Array.prototype.slice.call(document.querySelectorAll(".galerie a"));
  if (!links.length || typeof HTMLDialogElement === "undefined") return;

  var dialog = document.createElement("dialog");
  dialog.className = "lightbox";
  dialog.setAttribute("aria-label", "Bild in Großansicht");
  dialog.innerHTML =
    '<img alt="">' +
    '<div class="lightbox-leiste">' +
    '<button type="button" data-aktion="zurueck">&#8592; Zurück</button>' +
    '<button type="button" data-aktion="schliessen">Schließen</button>' +
    '<button type="button" data-aktion="weiter">Weiter &#8594;</button>' +
    "</div>";
  document.body.appendChild(dialog);
  var bild = dialog.querySelector("img");
  var aktuell = 0;

  function zeige(i) {
    aktuell = (i + links.length) % links.length;
    var a = links[aktuell];
    var vorschau = a.querySelector("img");
    bild.src = a.getAttribute("href");
    bild.alt = vorschau ? vorschau.alt : "";
  }

  links.forEach(function (a, i) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      zeige(i);
      dialog.showModal();
    });
  });

  dialog.addEventListener("click", function (e) {
    var aktion = e.target.getAttribute && e.target.getAttribute("data-aktion");
    if (aktion === "weiter") zeige(aktuell + 1);
    else if (aktion === "zurueck") zeige(aktuell - 1);
    else if (aktion === "schliessen" || e.target === dialog) dialog.close();
  });

  dialog.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight") zeige(aktuell + 1);
    if (e.key === "ArrowLeft") zeige(aktuell - 1);
  });

  dialog.addEventListener("close", function () {
    if (links[aktuell]) links[aktuell].focus();
  });
})();
