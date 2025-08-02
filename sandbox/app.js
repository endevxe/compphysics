// app.js

const canvas = document.getElementById("sandbox");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth * 0.7;
canvas.height = window.innerHeight * 0.7;

let components = [];

function addComponent(type) {
  const newComponent = {
    type,
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    properties: {
      mass: type === "mass" ? 1 : undefined,
      charge: type === "charge" ? 1 : undefined,
      k: type === "spring" ? 0.1 : undefined,
    },
  };
  components.push(newComponent);
  drawComponents();
}

function drawComponents() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  components.forEach((comp) => {
    ctx.beginPath();
    if (comp.type === "mass") {
      ctx.arc(comp.x, comp.y, 20, 0, Math.PI * 2);
      ctx.fillStyle = "blue";
    } else if (comp.type === "spring") {
      ctx.rect(comp.x, comp.y, 10, 40);
      ctx.fillStyle = "green";
    } else if (comp.type === "charge") {
      ctx.arc(comp.x, comp.y, 15, 0, Math.PI * 2);
      ctx.fillStyle = comp.properties.charge > 0 ? "red" : "purple";
    }
    ctx.fill();
  });
}

window.addEventListener("resize", () => {
  canvas.width = window.innerWidth * 0.7;
  canvas.height = window.innerHeight * 0.7;
  drawComponents();
});

document.getElementById("add-mass").addEventListener("click", () => addComponent("mass"));
document.getElementById("add-spring").addEventListener("click", () => addComponent("spring"));
document.getElementById("add-charge").addEventListener("click", () => addComponent("charge"));
document.getElementById("clear-canvas").addEventListener("click", () => {
  components = [];
  drawComponents();
});

// --- 3D / WebXR Integration ---

// Import Three.js & VRButton via CDN in HTML
// <script src="https://cdn.jsdelivr.net/npm/three@0.157.0/build/three.min.js"></script>
// <script src="https://cdn.jsdelivr.net/npm/three@0.157.0/examples/jsm/webxr/VRButton.js"></script>

const threeContainer = document.getElementById("three-view");
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.xr.enabled = true;
document.body.appendChild(VRButton.createButton(renderer));
threeContainer.appendChild(renderer.domElement);

camera.position.z = 5;

const light = new THREE.PointLight(0xffffff, 1);
light.position.set(10, 10, 10);
scene.add(light);

function generate3DObjects() {
  scene.clear();
  components.forEach((comp) => {
    let obj;
    if (comp.type === "mass") {
      const geometry = new THREE.SphereGeometry(0.2);
      const material = new THREE.MeshStandardMaterial({ color: 0x0000ff });
      obj = new THREE.Mesh(geometry, material);
    } else if (comp.type === "spring") {
      const geometry = new THREE.CylinderGeometry(0.05, 0.05, 0.5);
      const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
      obj = new THREE.Mesh(geometry, material);
    } else if (comp.type === "charge") {
      const geometry = new THREE.SphereGeometry(0.15);
      const color = comp.properties.charge > 0 ? 0xff0000 : 0x800080;
      const material = new THREE.MeshStandardMaterial({ color });
      obj = new THREE.Mesh(geometry, material);
    }
    if (obj) {
      obj.position.set((comp.x - canvas.width / 2) / 100, (canvas.height / 2 - comp.y) / 100, 0);
      scene.add(obj);
    }
  });
}

document.getElementById("view-3d").addEventListener("click", () => {
  generate3DObjects();
  renderer.setAnimationLoop(() => {
    renderer.render(scene, camera);
  });
});
