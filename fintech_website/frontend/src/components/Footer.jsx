import "../index.css";

export default function Footer() {
  return (
    <footer className="footer">
      <p>&copy; {new Date().getFullYear()} FinTechX. All rights reserved.</p>
    </footer>
  );
}
