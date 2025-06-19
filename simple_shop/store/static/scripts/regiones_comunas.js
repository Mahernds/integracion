const regionesYcomunas = {
  "Región de Valparaíso": ["Viña del Mar", "Valparaíso", "Quilpué", "Villa Alemana", "Concón", "Quintero", "San Antonio"],
  "Región Metropolitana": ["Santiago", "Puente Alto", "Maipú", "Las Condes", "La Florida", "Ñuñoa", "San Bernardo"],
  "Región del Biobío": ["Concepción", "Talcahuano", "Coronel", "San Pedro de la Paz"],
  "Región de La Araucanía": ["Temuco", "Padre Las Casas", "Angol"],
  "Región de Coquimbo": ["La Serena", "Coquimbo", "Ovalle"],
  "Región del Maule": ["Talca", "Curicó", "Linares"],
  "Región de Los Lagos": ["Puerto Montt", "Osorno", "Castro"],
  "Región de Antofagasta": ["Antofagasta", "Calama", "Tocopilla"],
  "Región de Tarapacá": ["Iquique", "Alto Hospicio"],
  "Región de Atacama": ["Copiapó", "Vallenar"],
  "Región de O’Higgins": ["Rancagua", "San Fernando", "Rengo"],
  "Región de Los Ríos": ["Valdivia", "La Unión"],
  "Región de Aysén": ["Coyhaique"],
  "Región de Magallanes": ["Punta Arenas"],
  "Región de Arica y Parinacota": ["Arica"]
};

document.addEventListener("DOMContentLoaded", function () {
  const regionSelect = document.getElementById("region");
  const comunaSelect = document.getElementById("comuna");

  if (regionSelect && comunaSelect) {
    for (const region in regionesYcomunas) {
      const option = document.createElement("option");
      option.value = region;
      option.textContent = region;
      regionSelect.appendChild(option);
    }

    regionSelect.addEventListener("change", function () {
      comunaSelect.innerHTML = '<option value="">Seleccione una comuna</option>';
      const comunas = regionesYcomunas[this.value] || [];
      comunas.forEach(comuna => {
        const option = document.createElement("option");
        option.value = comuna;
        option.textContent = comuna;
        comunaSelect.appendChild(option);
      });
    });
  }
});


