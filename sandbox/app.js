// app.js

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
    this.vx = 0; // Velocity X
    this.vy = 0; // Velocity Y
    this.ax = 0; // Acceleration X
    this.ay = 0; // Acceleration Y
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

    ctx.fillStyle = "#fff";
    ctx.font = "16px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(this.type, this.x, this.y + 5);
  }

  isHovered(mx, my) {
    return Math.hypot(this.x - mx, this.y - my) < this.size / 2;
  }

  applyPhysics() {
    if (this.mass) {
      this.vx += this.ax;
      this.vy += this.ay;
      this.x += this.vx;
      this.y += this.vy;
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
    c.ay = 0.1; // Simple gravity
    c.applyPhysics();
  }
}

function gameLoop() {
  updatePhysics();
  drawComponents();
  requestAnimationFrame(gameLoop);
}

document.querySelectorAll(".toolbox button").forEach((btn) => {
  btn.addEventListener("click", () => {
    const type = btn.getAttribute("data-type");
    components.push(new Component(type, canvas.width / 2, canvas.height / 2));
  });
});

canvas.addEventListener("mousedown", (e) => {
  const mx = e.offsetX;
  const my = e.offsetY;
  for (let c of components) {
    if (c.isHovered(mx, my)) {
      selectedComponent = c;
      isDragging = true;
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
  selectedComponent = null;
});

document.getElementById("vr-button").addEventListener("click", () => {
  alert("VR Mode is not yet implemented.");
});

gameLoop();
