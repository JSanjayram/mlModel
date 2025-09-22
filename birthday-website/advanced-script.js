let uploadedImage = null;
let scene, camera, renderer, universe = {};

// Initialize on load
window.addEventListener('load', () => {
    setTimeout(() => {
        document.getElementById('loading').style.display = 'none';
    }, 3000);
    
    initCustomCursor();
});

// Custom cursor tracking
function initCustomCursor() {
    document.addEventListener('mousemove', (e) => {
        document.body.style.setProperty('--cursor-x', e.clientX + 'px');
        document.body.style.setProperty('--cursor-y', e.clientY + 'px');
    });
}

// Handle image upload
document.getElementById('birthdayPersonImage').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            uploadedImage = e.target.result;
            // Add upload success effect
            gsap.to('.upload-wrapper', {
                scale: 1.1,
                duration: 0.3,
                yoyo: true,
                repeat: 1
            });
        };
        reader.readAsDataURL(file);
    }
});

// Launch the ultimate experience
function launchExperience() {
    const name = document.getElementById('birthdayPersonName').value;
    const message = document.getElementById('customMessage').value;
    const sender = document.getElementById('senderName').value;
    
    if (!name || !message || !sender) {
        // Error animation
        gsap.to('.create-section', {
            x: -20,
            duration: 0.1,
            yoyo: true,
            repeat: 5
        });
        return;
    }
    
    // Success launch animation
    gsap.to('.create-section', {
        scale: 0,
        rotation: 360,
        opacity: 0,
        duration: 1,
        ease: "power2.in",
        onComplete: () => {
            document.getElementById('createCard').style.display = 'none';
            document.getElementById('universe-container').style.display = 'block';
            
            // Update content
            document.getElementById('cosmic-title').textContent = `🌟 HAPPY BIRTHDAY ${name.toUpperCase()}! 🌟`;
            document.getElementById('message-constellation').textContent = message;
            document.getElementById('sender-signature').textContent = `From the Universe of: ${sender}`;
            
            if (uploadedImage) {
                document.getElementById('dimensional-image').src = uploadedImage;
            } else {
                document.getElementById('dimensional-image').src = `https://via.placeholder.com/400x400/ff0080/ffffff?text=${name.charAt(0)}`;
            }
            
            initQuantumUniverse();
        }
    });
}

// Initialize the quantum universe
function initQuantumUniverse() {
    const canvas = document.getElementById('universe-canvas');
    
    // Scene setup
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 2000);
    renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(0x000000, 0);
    
    // Create quantum particles
    createQuantumField();
    
    // Create dimensional portals
    createDimensionalPortals();
    
    // Create energy waves
    createEnergyWaves();
    
    // Create cosmic fireworks
    createCosmicFireworks();
    
    // Create floating love elements
    createFloatingElements();
    
    // Start universe animation
    animateUniverse();
    
    // Camera journey
    initCameraJourney();
}

// Create love-themed particle field
function createQuantumField() {
    const particleCount = 3000;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    const sizes = new Float32Array(particleCount);
    const types = new Float32Array(particleCount);
    
    for (let i = 0; i < particleCount; i++) {
        const i3 = i * 3;
        
        // Heart-shaped distribution
        const t = Math.random() * Math.PI * 2;
        const heartX = 16 * Math.sin(t) ** 3;
        const heartY = 13 * Math.cos(t) - 5 * Math.cos(2*t) - 2 * Math.cos(3*t) - Math.cos(4*t);
        const radius = Math.random() * 300 + 150;
        
        positions[i3] = (heartX + (Math.random() - 0.5) * 100) * (radius / 100);
        positions[i3 + 1] = (heartY + (Math.random() - 0.5) * 100) * (radius / 100);
        positions[i3 + 2] = (Math.random() - 0.5) * 400;
        
        // Love colors - pink, red, gold
        const colorType = Math.random();
        let color;
        if (colorType < 0.4) {
            color = new THREE.Color(0xff69b4); // Hot pink
        } else if (colorType < 0.7) {
            color = new THREE.Color(0xff1493); // Deep pink
        } else {
            color = new THREE.Color(0xffd700); // Gold
        }
        
        colors[i3] = color.r;
        colors[i3 + 1] = color.g;
        colors[i3 + 2] = color.b;
        
        sizes[i] = Math.random() * 8 + 2;
        types[i] = Math.floor(Math.random() * 3); // 0=heart, 1=star, 2=sparkle
    }
    
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
    
    const material = new THREE.ShaderMaterial({
        uniforms: {
            time: { value: 0 }
        },
        vertexShader: `
            attribute float size;
            varying vec3 vColor;
            uniform float time;
            
            void main() {
                vColor = color;
                vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
                gl_PointSize = size * (300.0 / -mvPosition.z) * (1.0 + sin(time + position.x * 0.01) * 0.5);
                gl_Position = projectionMatrix * mvPosition;
            }
        `,
        fragmentShader: `
            varying vec3 vColor;
            
            void main() {
                float r = distance(gl_PointCoord, vec2(0.5, 0.5));
                if (r > 0.5) discard;
                
                float alpha = 1.0 - r * 2.0;
                gl_FragColor = vec4(vColor, alpha);
            }
        `,
        transparent: true,
        vertexColors: true,
        blending: THREE.AdditiveBlending
    });
    
    const particles = new THREE.Points(geometry, material);
    scene.add(particles);
    universe.quantumField = particles;
}

// Create dimensional portals
function createDimensionalPortals() {
    const portals = [];
    
    for (let i = 0; i < 8; i++) {
        const geometry = new THREE.RingGeometry(20, 25, 32);
        const material = new THREE.ShaderMaterial({
            uniforms: {
                time: { value: 0 },
                color1: { value: new THREE.Color(0xff0080) },
                color2: { value: new THREE.Color(0x00ffff) }
            },
            vertexShader: `
                varying vec2 vUv;
                void main() {
                    vUv = uv;
                    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                }
            `,
            fragmentShader: `
                uniform float time;
                uniform vec3 color1;
                uniform vec3 color2;
                varying vec2 vUv;
                
                void main() {
                    float angle = atan(vUv.y - 0.5, vUv.x - 0.5);
                    float radius = distance(vUv, vec2(0.5));
                    
                    vec3 color = mix(color1, color2, sin(angle * 4.0 + time) * 0.5 + 0.5);
                    float alpha = sin(radius * 10.0 - time * 2.0) * 0.5 + 0.5;
                    
                    gl_FragColor = vec4(color, alpha * 0.8);
                }
            `,
            transparent: true,
            side: THREE.DoubleSide
        });
        
        const portal = new THREE.Mesh(geometry, material);
        portal.position.set(
            (Math.random() - 0.5) * 400,
            (Math.random() - 0.5) * 400,
            (Math.random() - 0.5) * 400
        );
        portal.rotation.set(
            Math.random() * Math.PI,
            Math.random() * Math.PI,
            Math.random() * Math.PI
        );
        
        scene.add(portal);
        portals.push(portal);
    }
    
    universe.portals = portals;
}

// Create energy waves
function createEnergyWaves() {
    const waves = [];
    
    for (let i = 0; i < 5; i++) {
        const geometry = new THREE.SphereGeometry(50 + i * 30, 32, 16);
        const material = new THREE.ShaderMaterial({
            uniforms: {
                time: { value: 0 }
            },
            vertexShader: `
                uniform float time;
                varying vec3 vPosition;
                
                void main() {
                    vPosition = position;
                    vec3 pos = position;
                    pos += normal * sin(time + position.y * 0.1) * 5.0;
                    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
                }
            `,
            fragmentShader: `
                uniform float time;
                varying vec3 vPosition;
                
                void main() {
                    float intensity = sin(time + vPosition.y * 0.1) * 0.5 + 0.5;
                    vec3 color = mix(vec3(1.0, 0.0, 0.5), vec3(0.0, 1.0, 1.0), intensity);
                    gl_FragColor = vec4(color, 0.1);
                }
            `,
            transparent: true,
            wireframe: true
        });
        
        const wave = new THREE.Mesh(geometry, material);
        scene.add(wave);
        waves.push(wave);
    }
    
    universe.waves = waves;
}

// Create friendship fireworks
function createCosmicFireworks() {
    const fireworks = [];
    
    for (let i = 0; i < 15; i++) {
        const particleCount = 150;
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const velocities = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);
        
        const centerX = (Math.random() - 0.5) * 400;
        const centerY = (Math.random() - 0.5) * 400;
        const centerZ = (Math.random() - 0.5) * 400;
        
        for (let j = 0; j < particleCount; j++) {
            const j3 = j * 3;
            
            positions[j3] = centerX;
            positions[j3 + 1] = centerY;
            positions[j3 + 2] = centerZ;
            
            // Heart-burst pattern
            const angle = (j / particleCount) * Math.PI * 2;
            const speed = Math.random() * 8 + 3;
            velocities[j3] = Math.cos(angle) * speed;
            velocities[j3 + 1] = Math.sin(angle) * speed;
            velocities[j3 + 2] = (Math.random() - 0.5) * 6;
            
            // Friendship colors - warm tones
            const friendColors = [
                new THREE.Color(0xff69b4), // Hot pink
                new THREE.Color(0xffd700), // Gold
                new THREE.Color(0xff6347), // Tomato
                new THREE.Color(0x98fb98), // Pale green
                new THREE.Color(0x87ceeb)  // Sky blue
            ];
            const color = friendColors[Math.floor(Math.random() * friendColors.length)];
            colors[j3] = color.r;
            colors[j3 + 1] = color.g;
            colors[j3 + 2] = color.b;
        }
        
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('velocity', new THREE.BufferAttribute(velocities, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        
        const material = new THREE.PointsMaterial({
            size: 3,
            vertexColors: true,
            transparent: true,
            opacity: 0.8,
            blending: THREE.AdditiveBlending
        });
        
        const firework = new THREE.Points(geometry, material);
        scene.add(firework);
        fireworks.push(firework);
    }
    
    universe.fireworks = fireworks;
}

// Camera journey focusing on uploaded image
function initCameraJourney() {
    camera.position.set(0, 0, 1000);
    camera.lookAt(0, 0, 0);
    
    gsap.timeline()
        .to(camera.position, {
            z: 300,
            duration: 3,
            ease: "power2.out"
        })
        .to(camera.rotation, {
            y: Math.PI * 2,
            duration: 6,
            ease: "power1.inOut"
        }, 0)
        .to(camera.position, {
            x: 0,
            y: 0,
            z: 150,
            duration: 4,
            ease: "power2.inOut",
            onComplete: () => {
                // Focus on the uploaded image
                focusOnImage();
            }
        }, 3);
}

// Focus camera on the uploaded image
function focusOnImage() {
    const imageElement = document.querySelector('.photo-frame');
    if (imageElement) {
        gsap.to(camera.position, {
            x: 0,
            y: 0,
            z: 100,
            duration: 2,
            ease: "power2.inOut"
        });
        
        // Highlight the image
        gsap.to('.photo-frame', {
            scale: 1.2,
            duration: 2,
            ease: "power2.inOut",
            yoyo: true,
            repeat: -1
        });
    }
}

// Main universe animation loop
function animateUniverse() {
    requestAnimationFrame(animateUniverse);
    
    const time = Date.now() * 0.001;
    
    // Animate quantum field
    if (universe.quantumField) {
        universe.quantumField.material.uniforms.time.value = time;
        universe.quantumField.rotation.y += 0.002;
    }
    
    // Animate portals
    if (universe.portals) {
        universe.portals.forEach((portal, i) => {
            portal.material.uniforms.time.value = time;
            portal.rotation.z += 0.01 + i * 0.002;
        });
    }
    
    // Animate waves
    if (universe.waves) {
        universe.waves.forEach((wave, i) => {
            wave.material.uniforms.time.value = time;
            wave.rotation.x += 0.005;
            wave.rotation.y += 0.003;
        });
    }
    
    // Animate fireworks
    if (universe.fireworks) {
        universe.fireworks.forEach(firework => {
            const positions = firework.geometry.attributes.position.array;
            const velocities = firework.geometry.attributes.velocity.array;
            
            for (let i = 0; i < positions.length; i += 3) {
                positions[i] += velocities[i] * 0.5;
                positions[i + 1] += velocities[i + 1] * 0.5;
                positions[i + 2] += velocities[i + 2] * 0.5;
                
                // Reset if too far
                if (Math.abs(positions[i]) > 300) {
                    positions[i] = (Math.random() - 0.5) * 600;
                    positions[i + 1] = (Math.random() - 0.5) * 600;
                    positions[i + 2] = (Math.random() - 0.5) * 600;
                }
            }
            
            firework.geometry.attributes.position.needsUpdate = true;
        });
    }
    
    // Animate floating love elements
    scene.children.forEach(child => {
        if (child.userData && child.userData.floatSpeed) {
            child.position.y = child.userData.originalY + Math.sin(time * child.userData.floatSpeed) * 15;
            child.rotation.x += 0.005;
            child.rotation.y += 0.008;
            child.rotation.z += 0.003;
        }
    });
    
    // Pulse effect for love particles
    if (universe.quantumField) {
        const scale = 1 + Math.sin(time * 2) * 0.1;
        universe.quantumField.scale.set(scale, scale, scale);
    }
    
    renderer.render(scene, camera);
}

// Create floating love elements
function createFloatingElements() {
    const shapes = [];
    
    // Create floating hearts and friendship symbols
    for (let i = 0; i < 25; i++) {
        let geometry, material;
        
        if (i < 15) {
            // Heart shapes
            geometry = new THREE.SphereGeometry(3, 8, 6);
            material = new THREE.MeshBasicMaterial({
                color: new THREE.Color(0xff69b4),
                transparent: true,
                opacity: 0.8
            });
        } else {
            // Star shapes for friendship
            geometry = new THREE.ConeGeometry(2, 4, 5);
            material = new THREE.MeshBasicMaterial({
                color: new THREE.Color(0xffd700),
                transparent: true,
                opacity: 0.7
            });
        }
        
        const element = new THREE.Mesh(geometry, material);
        element.position.set(
            (Math.random() - 0.5) * 300,
            (Math.random() - 0.5) * 300,
            (Math.random() - 0.5) * 300
        );
        
        // Add floating animation data
        element.userData = {
            originalY: element.position.y,
            floatSpeed: Math.random() * 0.02 + 0.01
        };
        
        scene.add(element);
        shapes.push(element);
    }
    
    universe.floatingElements = shapes;
    return shapes;

// Reset universe
function resetUniverse() {
    gsap.to('#universe-container', {
        opacity: 0,
        scale: 0,
        rotation: 360,
        duration: 1,
        onComplete: () => {
            document.getElementById('universe-container').style.display = 'none';
            document.getElementById('createCard').style.display = 'block';
            
            // Reset form
            document.getElementById('birthdayPersonName').value = '';
            document.getElementById('customMessage').value = '';
            document.getElementById('senderName').value = '';
            uploadedImage = null;
            
            // Cleanup 3D scene
            if (renderer) {
                renderer.dispose();
                scene = null;
                camera = null;
                renderer = null;
                universe = {};
            }
            
            // Animate form back in
            gsap.fromTo('.create-section', 
                { scale: 0, rotation: -360, opacity: 0 },
                { scale: 1, rotation: 0, opacity: 1, duration: 1, ease: "back.out(1.7)" }
            );
        }
    });
}

// Handle window resize
window.addEventListener('resize', () => {
    if (camera && renderer) {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }
});