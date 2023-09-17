const particles = []
let lastTime = 0

function update(time) {
  const deltaTime = time - lastTime

  lastTime = time

  for (const [index, particle] of particles.entries()) {
    const lifetime = time - particle.creationTime

    if (lifetime > particle.lifetime) {
      particle.element.remove()
      particles.splice(index, 1)

      continue
    }

    const lifetimePercentage = lifetime / particle.lifetime
    const nextLeftPosition = particle.element.offsetLeft + deltaTime * particle.velocity.x
    const nextTopPosition = particle.element.offsetTop + deltaTime * particle.velocity.y

    particle.element.style.left = `${nextLeftPosition}px`
    particle.element.style.top = `${nextTopPosition}px`
    particle.element.style.opacity = 1 - lifetimePercentage
  }

  // Recursively call update.
  requestAnimationFrame(update)
}

function randomIntInclusive(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

function randomSign() {
  return Math.random() < 0.5 ? -1 : 1
}

window.addEventListener("click", event => {
  const PARTICLE_AMOUNT_MIN = 3
  const PARTICLE_AMOUNT_MAX = 5
  const LIFETIME_MIN = 200
  const LIFETIME_MAX = 1000
  const particleAmount = randomIntInclusive(PARTICLE_AMOUNT_MIN, PARTICLE_AMOUNT_MAX)

  for (let i = 0; i < particleAmount; i++) {
    const particle = document.createElement("div")

    particle.className = "particle"
    particle.style.left = `${event.clientX}px`
    particle.style.top = `${event.clientY}px`
    document.body.appendChild(particle)

    const lifetime = randomIntInclusive(LIFETIME_MIN, LIFETIME_MAX)
    const theta = Math.random() * 2 * Math.PI
    const speed = Math.random() * 0.3 + 0.2

    particles.push({
      element: particle,
      lifetime,
      creationTime: performance.now(),
      velocity: {
        x: speed * Math.cos(theta) * randomSign(),
        y: speed * Math.sin(theta) * randomSign()
      }
    })
  }
})

window.addEventListener("load", () => {
  // Initialize particles.js.
  particlesJS.load("particles", "./assets/particle-config.json", () =>
    console.log("loaded particle config")
  )

  // Initialize Three.js.
  // const scene = document.getElementById("scene")
  // const parallaxInstance = new Parallax(scene)

  // Begin update loop.
  requestAnimationFrame(update)
})
