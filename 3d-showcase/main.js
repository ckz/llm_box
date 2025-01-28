import { initGame } from './game.js';
import { initFireworks } from './fireworks.js';

let currentScene = null;
let renderer, camera;

function init() {
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.getElementById('container').appendChild(renderer.domElement);

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5;

    window.addEventListener('resize', onWindowResize, false);

    document.getElementById('startGame').addEventListener('click', () => {
        if (currentScene) {
            currentScene.clear();
        }
        currentScene = initGame(renderer, camera);
        animate();
    });

    document.getElementById('showFireworks').addEventListener('click', () => {
        if (currentScene) {
            currentScene.clear();
        }
        currentScene = initFireworks(renderer, camera);
        animate();
    });
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
    requestAnimationFrame(animate);
    if (currentScene && currentScene.update) {
        currentScene.update();
    }
    renderer.render(currentScene.scene, camera);
}

init();