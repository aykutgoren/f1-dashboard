import '@testing-library/jest-dom'; // This imports jest-dom
import { render, screen } from '@testing-library/react';
import Home from './Home';

describe('Home Component', () => {
  it('renders the main heading and paragraph correctly', () => {
    // Render the Home component
    render(<Home />);

    // Check if the heading "F1 Dashboard" is in the document
    const heading = screen.getByText('F1 Dashboard');
    expect(heading).toBeInTheDocument();

    // Check if the paragraph with "Navigate to Dashboard" is in the document
    const paragraph = screen.getByText('Navigate to Dashboard to view summaries 🏎');
    expect(paragraph).toBeInTheDocument();
  });
});
