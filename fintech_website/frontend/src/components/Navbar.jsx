import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { isAuthenticated } = useAuth();
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };

    const handleResize = () => {
      setWindowWidth(window.innerWidth);
      if (window.innerWidth > 992) {
        setMenuOpen(false);
      }
    };

    window.addEventListener("scroll", handleScroll);
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("scroll", handleScroll);
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  const styles = {
    navbar: {
      position: "fixed",
      top: 0,
      left: 0,
      width: "100%",
      height: scrolled ? "60px" : "80px",
      backgroundColor: scrolled ? "rgba(255, 255, 255, 0.95)" : "#ffffff",
      boxShadow: "0 4px 20px rgba(0, 0, 0, 0.08)",
      zIndex: 1000,
      transition: "all 0.3s ease",
      backdropFilter: scrolled ? "blur(10px)" : "none",
    },
    navbarContainer: {
      maxWidth: "1200px",
      height: "100%",
      margin: "0 auto",
      padding: "0 1rem",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
    },
    logoText: {
      fontFamily: "'Poppins', sans-serif",
      fontSize: windowWidth <= 768 ? "1.5rem" : "1.8rem",
      fontWeight: 700,
      background: "linear-gradient(135deg, #4158D0, #C850C0)",
      WebkitBackgroundClip: "text",
      backgroundClip: "text",
      WebkitTextFillColor: "transparent",
      transition: "transform 0.3s ease",
    },
    navLinks: {
      display: windowWidth <= 992 ? (menuOpen ? "flex" : "none") : "flex",
      listStyle: "none",
      margin: 0,
      padding: windowWidth <= 992 ? "1rem 0" : 0,
      position: windowWidth <= 992 ? "fixed" : "static",
      top: scrolled ? "60px" : "80px",
      left: 0,
      width: windowWidth <= 992 ? "100%" : "auto",
      flexDirection: windowWidth <= 992 ? "column" : "row",
      alignItems: "center",
      backgroundColor: windowWidth <= 992 ? "#ffffff" : "transparent",
      boxShadow: windowWidth <= 992 ? "0 4px 20px rgba(0, 0, 0, 0.08)" : "none",
      zIndex: 999,
      transition: "all 0.3s ease",
    },
    navItem: {
      margin: windowWidth <= 992 ? "0.8rem 0" : "0 1rem",
      width: windowWidth <= 992 ? "100%" : "auto",
      textAlign: windowWidth <= 992 ? "center" : "left",
    },
    navLink: {
      fontFamily: "'Poppins', sans-serif",
      fontSize: windowWidth <= 768 ? "0.9rem" : "1rem",
      fontWeight: 500,
      color: "#333333",
      textDecoration: "none",
      padding: windowWidth <= 992 ? "0.8rem 0" : "0.5rem 0",
      position: "relative",
      display: "inline-block",
      transition: "color 0.3s ease",
      width: windowWidth <= 992 ? "100%" : "auto",
    },
    linkUnderline: {
      position: "absolute",
      bottom: 0,
      left: 0,
      width: "0%",
      height: "2px",
      background: "linear-gradient(135deg, #4158D0, #C850C0)",
      transition: "width 0.3s ease",
    },
    menuToggle: {
      display: windowWidth <= 992 ? "flex" : "none",
      flexDirection: "column",
      justifyContent: "space-between",
      width: "25px",
      height: "20px",
      cursor: "pointer",
      marginLeft: "auto",
      marginRight: "1rem",
      zIndex: 1001,
    },
    menuBar: {
      width: "100%",
      height: "2px",
      backgroundColor: "#333333",
      transition: "all 0.3s ease",
    },
    overlay: {
      display: menuOpen && windowWidth <= 992 ? "block" : "none",
      position: "fixed",
      top: 0,
      left: 0,
      width: "100%",
      height: "100%",
      backgroundColor: "rgba(0, 0, 0, 0.5)",
      zIndex: 998,
    },
  };

  const handleNavLinkHover = (e, isHovering) => {
    const underline = e.currentTarget.querySelector(".link-underline");
    if (underline) {
      underline.style.width = isHovering ? "100%" : "0%";
    }
    e.currentTarget.style.color = isHovering ? "#4158D0" : "#333333";
  };

  return (
    <>
      <nav style={styles.navbar}>
        <div style={styles.navbarContainer}>
          <Link to="/" style={{ textDecoration: "none" }}>
            <h1 style={styles.logoText}>EV Rentals</h1>
          </Link>

          <div style={styles.menuToggle} onClick={() => setMenuOpen(!menuOpen)}>
            <div
              style={{
                ...styles.menuBar,
                transform: menuOpen ? "translateY(9px) rotate(45deg)" : "none",
              }}
            ></div>
            <div
              style={{
                ...styles.menuBar,
                opacity: menuOpen ? 0 : 1,
              }}
            ></div>
            <div
              style={{
                ...styles.menuBar,
                transform: menuOpen
                  ? "translateY(-9px) rotate(-45deg)"
                  : "none",
              }}
            ></div>
          </div>

          <ul style={styles.navLinks}>
            <li style={styles.navItem}>
              <Link
                to="/"
                style={styles.navLink}
                onMouseEnter={(e) => handleNavLinkHover(e, true)}
                onMouseLeave={(e) => handleNavLinkHover(e, false)}
              >
                Home
                <span
                  className="link-underline"
                  style={styles.linkUnderline}
                ></span>
              </Link>
            </li>
            <li style={styles.navItem}>
              <Link
                to="/aboutus"
                style={styles.navLink}
                onMouseEnter={(e) => handleNavLinkHover(e, true)}
                onMouseLeave={(e) => handleNavLinkHover(e, false)}
              >
                About Us
                <span
                  className="link-underline"
                  style={styles.linkUnderline}
                ></span>
              </Link>
            </li>
            <li style={styles.navItem}>
              <Link
                to="/contactus"
                style={styles.navLink}
                onMouseEnter={(e) => handleNavLinkHover(e, true)}
                onMouseLeave={(e) => handleNavLinkHover(e, false)}
              >
                Contact
                <span
                  className="link-underline"
                  style={styles.linkUnderline}
                ></span>
              </Link>
            </li>
            {isAuthenticated ? (
              <>
                <li style={styles.navItem}>
                  <Link
                    to="/activity"
                    style={styles.navLink}
                    onMouseEnter={(e) => handleNavLinkHover(e, true)}
                    onMouseLeave={(e) => handleNavLinkHover(e, false)}
                  >
                    Activity
                    <span
                      className="link-underline"
                      style={styles.linkUnderline}
                    ></span>
                  </Link>
                </li>
                <li style={styles.navItem}>
                  <Link
                    to="/pay"
                    style={styles.navLink}
                    onMouseEnter={(e) => handleNavLinkHover(e, true)}
                    onMouseLeave={(e) => handleNavLinkHover(e, false)}
                  >
                    Pay
                    <span
                      className="link-underline"
                      style={styles.linkUnderline}
                    ></span>
                  </Link>
                </li>
              </>
            ) : (
              <li style={styles.navItem}>
                <Link
                  to="/login"
                  style={styles.navLink}
                  onMouseEnter={(e) => handleNavLinkHover(e, true)}
                  onMouseLeave={(e) => handleNavLinkHover(e, false)}
                >
                  Login
                  <span
                    className="link-underline"
                    style={styles.linkUnderline}
                  ></span>
                </Link>
              </li>
            )}
          </ul>
        </div>
      </nav>
      <div style={styles.overlay} onClick={() => setMenuOpen(false)} />
    </>
  );
}
