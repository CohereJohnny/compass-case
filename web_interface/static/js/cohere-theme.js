/**
 * Cohere Theme JavaScript
 * Enhances the user experience with animations and interactions 
 * that mimic Cohere's website behavior
 */

document.addEventListener('DOMContentLoaded', function() {
  // Animated blob decorations
  animateBlobs();
  
  // Add smooth scrolling
  setupSmoothScrolling();
  
  // Add hover effects to cards
  setupCardHoverEffects();
  
  // Add fade-in animations for content
  fadeInContent();
  
  // Handle navbar scrolling behavior
  setupNavbarScrollBehavior();
});

/**
 * Animate the blob decorations to slowly move and change
 */
function animateBlobs() {
  const blobs = document.querySelectorAll('.blob-decoration');
  
  if (blobs.length === 0) return;
  
  // Start animation loop
  let animationFrame;
  let startTime = Date.now();
  
  function animate() {
    const currentTime = Date.now();
    const elapsedTime = (currentTime - startTime) / 1000; // in seconds
    
    blobs.forEach((blob, index) => {
      // Calculate subtle movement using sine waves with different frequencies
      const xOffset = Math.sin(elapsedTime * 0.5 + index) * 10;
      const yOffset = Math.cos(elapsedTime * 0.3 + index) * 10;
      
      // Apply transform
      blob.style.transform = `translate(${xOffset}px, ${yOffset}px)`;
    });
    
    animationFrame = requestAnimationFrame(animate);
  }
  
  animate();
  
  // Cleanup on page unload
  window.addEventListener('beforeunload', () => {
    if (animationFrame) {
      cancelAnimationFrame(animationFrame);
    }
  });
}

/**
 * Setup smooth scrolling for anchor links
 */
function setupSmoothScrolling() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      
      if (targetId === '#') return;
      
      const targetElement = document.querySelector(targetId);
      
      if (targetElement) {
        e.preventDefault();
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
}

/**
 * Add subtle hover effects to cards
 */
function setupCardHoverEffects() {
  const cards = document.querySelectorAll('.card');
  
  cards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-5px)';
      this.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.1)';
      this.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
    });
    
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
      this.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.05)';
      this.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
    });
  });
}

/**
 * Add fade-in animations for content elements
 */
function fadeInContent() {
  // Create an Intersection Observer
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in');
        observer.unobserve(entry.target); // Stop observing once it's faded in
      }
    });
  }, {
    root: null, // Use viewport
    threshold: 0.1 // Trigger when 10% of the element is visible
  });
  
  // Observe content elements with the 'fade-in-element' class
  document.querySelectorAll('.fade-in-element').forEach(el => {
    observer.observe(el);
  });
}

/**
 * Change navbar appearance on scroll
 */
function setupNavbarScrollBehavior() {
  const navbar = document.querySelector('.navbar');
  
  if (!navbar) return;
  
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.classList.add('navbar-scrolled');
      navbar.style.boxShadow = '0 4px 10px rgba(0, 0, 0, 0.1)';
      navbar.style.backdropFilter = 'blur(10px)';
      navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
    } else {
      navbar.classList.remove('navbar-scrolled');
      navbar.style.boxShadow = '';
      navbar.style.backdropFilter = '';
      navbar.style.backgroundColor = '';
    }
  });
} 