// Get references to DOM elements
const canvas = document.getElementById("sandbox-canvas");
const ctx = canvas.getContext("2d");
const vrButton = document.getElementById("enter-vr");

canvas.width = canvas.clientWidth;
canvas.height = canvas.clientHeight;

let components = []; // Array to store placed components
let selectedComponent = null;

const componentTemplates = {
  mass: { type: "mass", width: 40, height: 40, color: "#4CAF50" },
  spring: { type: "spring", width: 10, height: 60, color: "#FFC107" },
  charge: { type: "charge", width: 30, height: 30, color: "#2196F3" },
};

// Drag-and-drop
let draggingTemplate = null;

function createComponent(template, x, y) {
  return { ...template, x: x - template.width / 2, y: y - template.height / 2 };
}

function drawComponent(comp) {
  ctx.fillStyle = comp.color;
  ctx.fillRect(comp.x, comp.y, comp.width, comp.height);
}

function render() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let comp of components) drawComponent(comp);
  requestAnimationFrame(render);
}
render();

canvas.addEventListener("mousedown", (e) => {
  const rect = canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  for (let comp of components) {
    if (
      x >= comp.x &&
      x <= comp.x + comp.width &&
      y >= comp.y &&
      y <= comp.y + comp.height
    ) {
      selectedComponent = comp;
      break;
    }
  }
});

canvas.addEventListener("mousemove", (e) => {
  if (selectedComponent) {
    const rect = canvas.getBoundingClientRect();
    selectedComponent.x = e.clientX - rect.left - selectedComponent.width / 2;
    selectedComponent.y = e.clientY - rect.top - selectedComponent.height / 2;
  }
});

canvas.addEventListener("mouseup", () => {
  selectedComponent = null;
});

// Template dragging
const templateElements = document.querySelectorAll(".template");

templateElements.forEach((el) => {
  el.addEventListener("dragstart", (e) => {
    draggingTemplate = componentTemplates[el.dataset.type];
  });
});

canvas.addEventListener("dragover", (e) => e.preventDefault());
canvas.addEventListener("drop", (e) => {
  if (draggingTemplate) {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const newComp = createComponent(draggingTemplate, x, y);
    components.push(newComp);
    draggingTemplate = null;
  }
});

// Placeholder VR logic
vrButton.addEventListener("click", () => {
