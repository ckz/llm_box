export function initGame(renderer, camera) {
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);

    // Player paddle
    const paddleGeometry = new THREE.BoxGeometry(1, 0.2, 0.2);
    const paddleMaterial = new THREE.MeshPhongMaterial({ color: 0x00ff00 });
    const paddle = new THREE.Mesh(paddleGeometry, paddleMaterial);
    paddle.position.y = -2;
    scene.add(paddle);

    // Lighting
    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(0, 1, 1);
    scene.add(light);
    scene.add(new THREE.AmbientLight(0x404040));

    // Game state
    let score = 0;
    let cubes = [];
    let gameSpeed = 0.02;
    const scoreElement = document.getElementById('scoreValue');

    // Mouse movement
    let mouseX = 0;
    renderer.domElement.addEventListener('mousemove', (event) => {
        mouseX = (event.clientX / window.innerWidth) * 2 - 1;
        paddle.position.x = THREE.MathUtils.clamp(mouseX * 3, -2.5, 2.5);
    });

    // Create a new cube
    function createCube() {
        const size = 0.3;
        const geometry = new THREE.BoxGeometry(size, size, size);
        const material = new THREE.MeshPhongMaterial({
            color: Math.random() * 0xffffff
        });
        const cube = new THREE.Mesh(geometry, material);
        cube.position.x = (Math.random() - 0.5) * 5;
        cube.position.y = 3;
        scene.add(cube);
        cubes.push(cube);
    }

    // Spawn cubes periodically
    setInterval(createCube, 2000);

    function checkCollision(cube, paddle) {
        const paddleBox = new THREE.Box3().setFromObject(paddle);
        const cubeBox = new THREE.Box3().setFromObject(cube);
        return paddleBox.intersectsBox(cubeBox);
    }

    function update() {
        // Update cubes
        for (let i = cubes.length - 1; i >= 0; i--) {
            const cube = cubes[i];
            cube.position.y -= gameSpeed;
            cube.rotation.x += 0.02;
            cube.rotation.y += 0.02;

            // Check for collision with paddle
            if (checkCollision(cube, paddle)) {
                score += 10;
                scoreElement.textContent = score;
                scene.remove(cube);
                cubes.splice(i, 1);
                gameSpeed += 0.001; // Increase difficulty
            }
            // Remove cubes that fall below the paddle
            else if (cube.position.y < -3) {
                scene.remove(cube);
                cubes.splice(i, 1);
            }
        }
    }

    function clear() {
        cubes.forEach(cube => scene.remove(cube));
        cubes = [];
        scene.clear();
    }

    return {
        scene,
        update,
        clear
    };
}