const game = document.getElementById("game");
const plane = document.getElementById("plane");
const speedLabel = document.getElementById("speed");
const statusLabel = document.getElementById("status");

const state = {
  x: window.innerWidth * 0.5,
  y: window.innerHeight * 0.42,
  speed: 120,
  heading: 0,
  pitch: 0,
  cameraX: 0,
  cameraY: 0
};

const keys = {};
const initialState = JSON.parse(JSON.stringify(state));

window.addEventListener("keydown", (e) => {
  keys[e.key] = true;
});

window.addEventListener("keyup", (e) => {
  keys[e.key] = false;
});

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function updateSpeed() {
  if (keys["w"] || keys["W"]) {
    state.speed += 0.7;
  }
  if (keys["s"] || keys["S"]) {
    state.speed -= 0.9;
  }
  state.speed = clamp(state.speed, 60, 240);
}

function updateTurn() {
  if (keys["a"] || keys["A"]) {
    state.heading -= 1.6;
  }
  if (keys["d"] || keys["D"]) {
    state.heading += 1.6;
  }
}

function updatePitch() {
  if (keys["ArrowUp"]) {
    state.pitch -= 0.8;
  }
  if (keys["ArrowDown"]) {
    state.pitch += 0.8;
  }
  state.pitch = clamp(state.pitch, -18, 18);
}

function updatePosition() {
  const radians = state.heading * Math.PI / 180;
  const forward = state.speed * 0.03;

  state.x += Math.sin(radians) * forward;
  state.y += state.pitch * 0.15;

  state.x = clamp(state.x, 40, window.innerWidth - 40);
  state.y = clamp(state.y, 80, window.innerHeight - 140);
}

function updateCamera() {
  // Intentionally too abrupt to create visible jitter for the benchmark.
  state.cameraX += (state.x - window.innerWidth * 0.5 - state.cameraX) * 0.35;
  state.cameraY += (state.y - window.innerHeight * 0.42 - state.cameraY) * 0.35;
  game.style.transform = `translate(${-state.cameraX}px, ${-state.cameraY}px)`;
}

function renderPlane() {
  plane.style.left = `${state.x}px`;
  plane.style.top = `${state.y}px`;
  plane.style.transform = `translate(-50%, -50%) rotate(${state.heading}deg) skewX(${state.pitch * 0.2}deg)`;
}

function renderHud() {
  // Intentionally wrong: it does not always reflect the latest speed in a clean way.
  statusLabel.textContent = state.speed < 90 ? "Status: Slow" : "Status: Flying";
}

function tick() {
  updateSpeed();
  updateTurn();
  updatePitch();
  updatePosition();
  updateCamera();
  renderPlane();
  renderHud();
  requestAnimationFrame(tick);
}

tick();
