export function initFireworks(renderer, camera) {
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);

    // Particle system for fireworks
    const particles = [];
    const explosions = [];

    class Particle {
        constructor(position, velocity, color) {
            const geometry = new THREE.SphereGeometry(0.02, 8, 8);
            const material = new THREE.MeshBasicMaterial({ color });
            this.mesh = new THREE.Mesh(geometry, material);
            this.mesh.position.copy(position);
            this.velocity = velocity;
            this.age = 0;
            scene.add(this.mesh);
        }

        update() {
            this.velocity.y -= 0.001; // gravity
            this.mesh.position.add(this.velocity);
            this.age += 0.016;
            return this.age < 2; // lifetime of 2 seconds
        }
    }

    class Explosion {
        constructor(position) {
            const particleCount = 100;
            this.particles = [];
            const color = new THREE.Color(Math.random() * 0xffffff);

            for (let i = 0; i < particleCount; i++) {
                const angle = Math.random() * Math.PI * 2;
                const phi = Math.random() * Math.PI * 2;
                const speed = 0.02 + Math.random() * 0.03;
                const velocity = new THREE.Vector3(
                    Math.sin(angle) * Math.cos(phi) * speed,
                    Math.cos(angle) * speed,
                    Math.sin(angle) * Math.sin(phi) * speed
                );
                this.particles.push(new Particle(position.clone(), velocity, color));
            }
        }

        update() {
            this.particles = this.particles.filter(particle => {
                const alive = particle.update();
                if (!alive) {
                    scene.remove(particle.mesh);
                }
                return alive;
            });
            return this.particles.length > 0;
        }
    }

    function launchFirework() {
        const x = (Math.random() - 0.5) * 4;
        const z = (Math.random() - 0.5) * 4;
        const position = new THREE.Vector3(x, -2, z);
        const velocity = new THREE.Vector3(0, 0.1, 0);
        const color = 0xffffff;
        const rocket = new Particle(position, velocity, color);
        particles.push(rocket);

        setTimeout(() => {
            scene.remove(rocket.mesh);
            const explosionPos = rocket.mesh.position.clone();
            explosions.push(new Explosion(explosionPos));
        }, 1000);
    }

    // Launch fireworks periodically
    setInterval(launchFirework, 2000);

    function update() {
        // Update particles
        particles.forEach((particle, i) => {
            if (!particle.update()) {
                scene.remove(particle.mesh);
                particles.splice(i, 1);
            }
        });

        // Update explosions
        explosions.forEach((explosion, i) => {
            if (!explosion.update()) {
                explosions.splice(i, 1);
            }
        });
    }

    function clear() {
        particles.forEach(particle => scene.remove(particle.mesh));
        explosions.forEach(explosion => {
            explosion.particles.forEach(particle => scene.remove(particle.mesh));
        });
        particles.length = 0;
        explosions.length = 0;
        scene.clear();
    }

    // Initial firework
    launchFirework();

    return {
        scene,
        update,
        clear
    };
}