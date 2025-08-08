// app.js (Sandbox)

const canvas = document.getElementById("sandbox-canvas");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let components = [];
let selectedComponent = null;
let isDragging = false;

class Component {
  constructor(type, x, y) {
    this.type = type;
    this.x = x;
    this.y = y;
    this.size = 50;
    this.color = this.getColor();
    this.mass = type === "mass" ? 1.0 : null;
    this.charge = type === "charge" ? 1.0 : null;
    this.k = type === "spring" ? 100 : null; // Spring constant
    this.vx = 0;
    this.vy = 0;
    this.ax = 0;
    this.ay = 0;
  }

  getColor() {
    switch (this.type) {
      case "mass": return "#ff6b6b";
      case "spring": return "#4ecdc4";
      case "charge": return "#ffe66d";
      default: return "#ccc";
    }
  }

  draw(ctx) {
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size / 2, 0, Math.PI * 2);
    ctx.fill();

    // Label
    ctx.fillStyle = "#fff";
    ctx.font = "16px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(this.type, this.x, this.y + 5);

    // Selection highlight
    if (this === selectedComponent) {
      ctx.strokeStyle = "#ffffff";
      ctx.lineWidth = 2;
      ctx.stroke();
    }
  }

  isHovered(mx, my) {
    return Math.hypot(this.x - mx, this.y - my) < this.size / 2;
  }

  applyPhysics() {
    if (this.mass) {
      this.vx += this.ax;
      this.vy += this.ay;

      // Friction
      this.vx *= 0.99;
      this.vy *= 0.99;

      // Update position
      this.x += this.vx;
      this.y += this.vy;

      // Boundaries
      if (this.x < this.size / 2) { this.x = this.size / 2; this.vx *= -0.7; }
      if (this.x > canvas.width - this.size / 2) { this.x = canvas.width - this.size / 2; this.vx *= -0.7; }
      if (this.y < this.size / 2) { this.y = this.size / 2; this.vy *= -0.7; }
      if (this.y > canvas.height - this.size / 2) { this.y = canvas.height - this.size / 2; this.vy *= -0.7; }
    }
  }
}

function drawComponents() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let c of components) {
    c.draw(ctx);
  }
}

function updatePhysics() {
  for (let c of components) {
    c.ax = 0;
    c.ay = 0.1; // gravity
    c.applyPhysics();
  }
}

function gameLoop() {
  updatePhysics();
  drawComponents();
  requestAnimationFrame(gameLoop);
}

// Toolbox click → add component
document.querySelectorAll(".toolbox button").forEach((btn) => {
  btn.addEventListener("click", () => {
    const type = btn.getAttribute("data-type");
    components.push(new Component(type, canvas.width / 2, canvas.height / 2));
  });
});

canvas.addEventListener("mousedown", (e) => {
  const mx = e.offsetX;
  const my = e.offsetY;
  selectedComponent = null;
  for (let c of components) {
    if (c.isHovered(mx, my)) {
      selectedComponent = c;
      isDragging = true;
      updatePropertiesPanel(c);
      break;
    }
  }
});

canvas.addEventListener("mousemove", (e) => {
  if (isDragging && selectedComponent) {
    selectedComponent.x = e.offsetX;
    selectedComponent.y = e.offsetY;
  }
});

canvas.addEventListener("mouseup", () => {
  isDragging = false;
});

// Delete selected component with Delete key
document.addEventListener("keydown", (e) => {
  if (e.key === "Delete" && selectedComponent) {
    components = components.filter(c => c !== selectedComponent);
    selectedComponent = null;
    clearPropertiesPanel();
  }
});

document.getElementById("vr-button").addEventListener("click", () => {
  alert("VR Mode is not yet implemented.");
});

// Update properties panel
function updatePropertiesPanel(component) {
  const panel = document.getElementById("properties-panel");
  panel.innerHTML = `
    <h3>Properties</h3>
    <p>Type: ${component.type}</p>
    ${component.mass !== null ? `<label>Mass: <input type="number" value="${component.mass}" step="0.1" id="prop-mass"></label>` : ""}
    ${component.charge !== null ? `<label>Charge: <input type="number" value="${component.charge}" step="0.1" id="prop-charge"></label>` : ""}
    ${component.k !== null ? `<label>Spring k: <input type="number" value="${component.k}" step="1" id="prop-k"></label>` : ""}
  `;

  if (component.mass !== null) {
    document.getElementById("prop-mass").addEventListener("input", (e) => {
      component.mass = parseFloat(e.target.value);
    });
  }
  if (component.charge !== null) {
    document.getElementById("prop-charge").addEventListener("input", (e) => {
      component.charge = parseFloat(e.target.value);
    });
  }
  if (component.k !== null) {
    document.getElementById("prop-k").addEventListener("input", (e) => {
      component.k = parseFloat(e.target.value);
    });
  }
}

function clearPropertiesPanel() {
  document.getElementById("properties-panel").innerHTML = "<h3>Properties</h3><p>Select a component</p>";
}

gameLoop();
