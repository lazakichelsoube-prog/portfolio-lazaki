/* =========================================================
   Portfolio — Lazaki Chelsoube
   Connecte le frontend statique a l'API Django (DRF).
   ========================================================= */

const API_BASE = ["localhost", "127.0.0.1"].includes(location.hostname)
  ? "http://127.0.0.1:8000/api"
  : "https://portfolio-lazaki.onrender.com/api";

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("anneeCourante").textContent = new Date().getFullYear();

  initNavToggle();
  chargerProfil();
  chargerCompetences();
  chargerParcours();
  chargerProjets();
  chargerCollaborations();
  initFormulaireContact();
});

/* ---------- Navigation mobile ---------- */
function initNavToggle() {
  const toggle = document.getElementById("navToggle");
  const nav = document.getElementById("mainNav");

  toggle.addEventListener("click", () => {
    const ouvert = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(ouvert));
  });

  nav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      nav.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
    });
  });
}

/* ---------- Profil (Hero + A propos) ---------- */
async function chargerProfil() {
  try {
    const res = await fetch(`${API_BASE}/profile/`);
    if (!res.ok) return;
    const profil = await res.json();
    if (!profil || Object.keys(profil).length === 0) return;

    setTexte("heroNom", profil.nom_complet);
    setTexte("heroTitre", profil.titre);
    setTexte("heroBio", profil.bio);
    setTexte("aproposBio", profil.bio);
    if (profil.processus_travail) {
      setTexte("aproposProcessus", profil.processus_travail);
    }

    if (profil.email) {
      const lienEmail = document.getElementById("contactEmail");
      lienEmail.textContent = profil.email;
      lienEmail.href = `mailto:${profil.email}`;
    }
    if (profil.github) {
      document.getElementById("contactGithub").href = profil.github;
    }
    if (profil.instagram) {
      document.getElementById("contactInstagram").href = profil.instagram;
    }

    if (profil.photo) {
      const img = document.getElementById("heroPhotoImg");
      const placeholder = document.getElementById("heroPhotoPlaceholder");
      img.src = profil.photo;
      img.style.display = "block";
      placeholder.style.display = "none";
    }
  } catch (erreur) {
    console.warn("Impossible de charger le profil depuis l'API :", erreur);
  }
}

/* ---------- Logos des competences ---------- */
const LOGOS_COMPETENCES = {
  "python": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg",
  "django": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/django/django-plain.svg",
  "javascript": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg",
  "php": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/php/php-original.svg",
  "java": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/java/java-original.svg",
  "html / css": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/html5/html5-original.svg",
  "mysql": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mysql/mysql-original.svg",
  "postgresql": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg",
};

const ICONES_PERSONNALISEES = {
  "réseaux cisco (ccna)": `<svg viewBox="0 0 24 24" fill="none" stroke="#FF6A1F" stroke-width="1.8"><circle cx="4" cy="12" r="2"/><circle cx="20" cy="5" r="2"/><circle cx="20" cy="19" r="2"/><path d="M6 12h6M12 12l6-5.5M12 12l6 5.5"/></svg>`,
  "modélisation uml": `<svg viewBox="0 0 24 24" fill="none" stroke="#FF6A1F" stroke-width="1.8"><rect x="3" y="3" width="7" height="6" rx="1"/><rect x="14" y="3" width="7" height="6" rx="1"/><rect x="8.5" y="15" width="7" height="6" rx="1"/><path d="M6.5 9v3.5h11V9M12 12.5V15"/></svg>`,
};

function getIconeHTML(nom) {
  const cle = nom.trim().toLowerCase();
  if (LOGOS_COMPETENCES[cle]) return `<img src="${LOGOS_COMPETENCES[cle]}" alt="" loading="lazy">`;
  if (ICONES_PERSONNALISEES[cle]) return ICONES_PERSONNALISEES[cle];
  return `<svg viewBox="0 0 24 24" fill="none" stroke="#FF6A1F" stroke-width="1.8"><path d="M8 9 4 12l4 3M16 9l4 3-4 3M13 6l-2 12"/></svg>`;
}

/* ---------- Competences ---------- */
async function chargerCompetences() {
  const conteneur = document.getElementById("skillsContainer");
  try {
    const res = await fetch(`${API_BASE}/skills/`);
    if (!res.ok) throw new Error("Réponse API invalide");
    const data = await res.json();
    const competences = data.results ?? data;

    if (!competences.length) {
      conteneur.innerHTML = '<p class="empty-text">Compétences à venir.</p>';
      return;
    }

    const groupes = {};
    competences.forEach((c) => {
      if (!groupes[c.categorie_affichage]) groupes[c.categorie_affichage] = [];
      groupes[c.categorie_affichage].push(c);
    });

    conteneur.innerHTML = Object.entries(groupes)
      .map(([nomGroupe, items]) => `
        <div class="skills-group">
          <h3>${escapeHtml(nomGroupe)}</h3>
          <div class="skill-chips">
            ${items.map((c) => `
              <div class="skill-chip">
                <span class="skill-chip__icon">${getIconeHTML(c.nom)}</span>
                <span class="skill-chip__label">${escapeHtml(c.nom)}</span>
              </div>`).join("")}
          </div>
        </div>`)
      .join("");
  } catch (erreur) {
    conteneur.innerHTML = '<p class="empty-text">Impossible de charger les compétences pour le moment.</p>';
    console.warn(erreur);
  }
}

/* ---------- Parcours ---------- */
async function chargerParcours() {
  const conteneur = document.getElementById("parcoursContainer");
  try {
    const res = await fetch(`${API_BASE}/etapes/`);
    if (!res.ok) throw new Error("Réponse API invalide");
    const data = await res.json();
    const etapes = data.results ?? data;

    if (!etapes.length) {
      conteneur.innerHTML = '<p class="empty-text">Parcours à venir.</p>';
      return;
    }

    conteneur.innerHTML = etapes.map((e) => `
      <div class="timeline-item">
        <div class="timeline-item__dot"></div>
        <div class="timeline-item__content">
          <p class="timeline-item__date">${escapeHtml(e.periode)}</p>
          <h3>${escapeHtml(e.titre)}</h3>
          <p>${escapeHtml(e.description)}</p>
        </div>
      </div>
    `).join("");
  } catch (erreur) {
    conteneur.innerHTML = '<p class="empty-text">Impossible de charger le parcours pour le moment.</p>';
    console.warn(erreur);
  }
}

/* ---------- Projets ---------- */
async function chargerProjets() {
  const conteneur = document.getElementById("projectsContainer");
  try {
    const res = await fetch(`${API_BASE}/projects/`);
    if (!res.ok) throw new Error("Réponse API invalide");
    const data = await res.json();
    const projets = data.results ?? data;

    if (!projets.length) {
      conteneur.innerHTML = '<p class="empty-text">Aucun projet publié pour le moment — revenez bientôt !</p>';
      return;
    }

    conteneur.innerHTML = projets.map((p) => `
      <article class="project-card">
        ${p.image ? `<img src="${p.image}" alt="Aperçu du projet ${escapeHtml(p.titre)}">` : ""}
        <h3>${escapeHtml(p.titre)}</h3>
        <p>${escapeHtml(p.description)}</p>
        <div class="tech-tags">
          ${(p.technologies_list || []).map((t) => `<span class="tech-tag">${escapeHtml(t)}</span>`).join("")}
        </div>
        <div class="project-links">
          ${p.lien_demo ? `<a href="${p.lien_demo}" target="_blank" rel="noopener">Démo</a>` : ""}
          ${p.lien_code ? `<a href="${p.lien_code}" target="_blank" rel="noopener">Code source</a>` : ""}
        </div>
      </article>
    `).join("");
  } catch (erreur) {
    conteneur.innerHTML = '<p class="empty-text">Impossible de charger les réalisations pour le moment.</p>';
    console.warn(erreur);
  }
}

/* ---------- Collaborations / clients ---------- */
async function chargerCollaborations() {
  const conteneur = document.getElementById("clientsContainer");
  try {
    const res = await fetch(`${API_BASE}/clients/`);
    if (!res.ok) throw new Error("Réponse API invalide");
    const data = await res.json();
    const clients = data.results ?? data;

    if (!clients.length) return;

    conteneur.innerHTML = clients.map((c) => `
      <div class="client-card">
        <h3>${escapeHtml(c.nom)}</h3>
        ${c.temoignage ? `<p>${escapeHtml(c.temoignage)}</p>` : ""}
        ${c.lien ? `<a href="${c.lien}" target="_blank" rel="noopener">Voir le lien →</a>` : ""}
      </div>
    `).join("");
  } catch (erreur) {
    console.warn("Impossible de charger les collaborations :", erreur);
  }
}

/* ---------- Formulaire de contact ---------- */
function initFormulaireContact() {
  const form = document.getElementById("contactForm");
  const feedback = document.getElementById("formFeedback");
  const bouton = document.getElementById("contactSubmit");

  form.addEventListener("submit", async (evenement) => {
    evenement.preventDefault();
    feedback.textContent = "";
    feedback.className = "form-feedback";

    const donnees = {
      nom: form.nom.value.trim(),
      email: form.email.value.trim(),
      sujet: form.sujet.value.trim(),
      contenu: form.contenu.value.trim(),
    };

    if (!donnees.nom || !donnees.email || !donnees.contenu) {
      feedback.textContent = "Merci de remplir tous les champs obligatoires.";
      feedback.classList.add("error");
      return;
    }

    bouton.disabled = true;
    bouton.textContent = "Envoi en cours…";

    try {
      const res = await fetch(`${API_BASE}/messages/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(donnees),
      });

      if (!res.ok) throw new Error("Le serveur a refusé le message.");

      feedback.textContent = "Message envoyé avec succès. Merci, je vous répondrai rapidement !";
      feedback.classList.add("success");
      form.reset();
    } catch (erreur) {
      feedback.textContent = "L'envoi a échoué. Vérifiez que le serveur Django est bien lancé, ou écrivez-moi directement par email.";
      feedback.classList.add("error");
      console.warn(erreur);
    } finally {
      bouton.disabled = false;
      bouton.textContent = "Envoyer le message";
    }
  });
}

/* ---------- Utilitaires ---------- */
function setTexte(id, valeur) {
  const el = document.getElementById(id);
  if (el && valeur) el.textContent = valeur;
}

function escapeHtml(chaine) {
  const div = document.createElement("div");
  div.textContent = chaine ?? "";
  return div.innerHTML;
}