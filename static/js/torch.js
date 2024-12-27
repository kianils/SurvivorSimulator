import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';

export default class TorchComponent extends Component {
  @tracked embers = [];

  constructor() {
    super(...arguments);
    this.createEmbers();
  }

  createEmbers() {
    setInterval(() => {
      const newEmber = {
        id: Math.random(), // Unique identifier
        x: Math.random() * 100 - 50, // Random horizontal offset (-50% to 50%)
        size: Math.random() * 8 + 4, // Random size (4px to 12px)
        duration: Math.random() * 3 + 2, // Random animation duration (2s to 5s)
      };

      this.embers = [...this.embers, newEmber];

      // Keep the number of embers manageable
      if (this.embers.length > 100) {
        this.embers.shift(); // Remove the oldest ember
      }
    }, 200); // Generate a new ember every 200ms
  }
}