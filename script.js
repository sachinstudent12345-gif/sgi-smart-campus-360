// ==========================================
// SGI SMART CAMPUS 360
// Main JavaScript
// ==========================================


// LOGIN MODAL
function openLogin() {
    const modal = document.getElementById("loginModal");

    if (modal) {
        modal.classList.add("active");
        document.body.style.overflow = "hidden";
    }
}


// CLOSE LOGIN MODAL
function closeLogin() {
    const modal = document.getElementById("loginModal");

    if (modal) {
        modal.classList.remove("active");
        document.body.style.overflow = "auto";
    }
}
// REGISTRATION MODAL
function openRegister() {
    const modal = document.getElementById("registerModal");

    if (modal) {
        modal.classList.add("active");
        document.body.style.overflow = "hidden";
    }
}

function closeRegister() {
    const modal = document.getElementById("registerModal");

    if (modal) {
        modal.classList.remove("active");
        document.body.style.overflow = "auto";
    }
}

// CLOSE MODAL WHEN CLICKING OUTSIDE
window.addEventListener("click", function (event) {

    const modal = document.getElementById("loginModal");

    if (event.target === modal) {
        closeLogin();
    }

});


// ESC KEY TO CLOSE MODAL
document.addEventListener("keydown", function (event) {

    if (event.key === "Escape") {
        closeLogin();
    }

});


async function demoLogin() {

    const id = document.querySelector(
        'input[placeholder="Enter your ID"]'
    );

    const password = document.querySelector(
        'input[placeholder="Enter password"]'
    );

    if (!id.value.trim() || !password.value.trim()) {

        alert("⚠️ Please enter your Campus ID and Password.");

        return;
    }

    try {

        const response = await fetch("/api/login", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                campus_id: id.value.trim(),
                password: password.value.trim()
            })

        });

        const data = await response.json();

        if (data.success) {

            localStorage.setItem(
                "student",
                JSON.stringify(data.student)
            );

            window.location.href = "/dashboard.html";

        } else {

            alert("❌ " + data.message);

        }

    } catch (error) {

        console.error(error);

        alert(
            "⚠️ Server connection problem.\n" +
            "Please make sure Flask server is running."
        );

    }
}

// SMOOTH SCROLLING
document.querySelectorAll('a[href^="#"]').forEach(function (link) {

    link.addEventListener("click", function (event) {

        const targetId = this.getAttribute("href");

        const target = document.querySelector(targetId);

        if (target) {

            event.preventDefault();

            target.scrollIntoView({
                behavior: "smooth"
            });

        }

    });

});


// NAVBAR SCROLL EFFECT
window.addEventListener("scroll", function () {

    const navbar = document.querySelector(".navbar");

    if (!navbar) return;

    if (window.scrollY > 50) {

        navbar.classList.add("scrolled");

    } else {

        navbar.classList.remove("scrolled");

    }

});


// PAGE LOAD ANIMATION
window.addEventListener("load", function () {

    document.body.classList.add("loaded");

});
// ==========================================
// STUDENT REGISTRATION
// ==========================================

async function registerStudent() {

    const name = document.getElementById("registerName").value.trim();
    const campusId = document.getElementById("registerCampusId").value.trim();
    const branch = document.getElementById("registerBranch").value;
    const semester = document.getElementById("registerSemester").value;
    const password = document.getElementById("registerPassword").value;

    if (!name || !campusId || !branch || !semester || !password) {
        alert("⚠️ Please fill all registration fields.");
        return;
    }

    try {

        const response = await fetch("/api/register", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                name: name,
                campus_id: campusId,
                branch: branch,
                semester: semester,
                password: password
            })

        });

        const data = await response.json();

        if (data.success) {

            alert("✅ Account created successfully!");

            closeRegister();

            // Clear form
            document.getElementById("registerName").value = "";
            document.getElementById("registerCampusId").value = "";
            document.getElementById("registerBranch").value = "";
            document.getElementById("registerSemester").value = "";
            document.getElementById("registerPassword").value = "";

        } else {

            alert("❌ " + data.message);

        }

    } catch (error) {

        console.error(error);

        alert(
            "⚠️ Server connection problem.\n" +
            "Please make sure Flask server is running."
        );
    }
}
// ==========================================
// SMART COMPLAINTS
// ==========================================

function openComplaints() {

    const modal =
        document.getElementById("complaintModal");

    if (modal) {

        modal.classList.add("active");

        document.body.style.overflow = "hidden";
    }
}


function closeComplaints() {

    const modal =
        document.getElementById("complaintModal");

    if (modal) {

        modal.classList.remove("active");

        document.body.style.overflow = "auto";
    }
}


// ==========================================
// SUBMIT COMPLAINT
// ==========================================

async function submitComplaint() {

    const studentData =
        localStorage.getItem("student");

    if (!studentData) {

        alert("⚠️ Please login first.");

        window.location.href = "/";

        return;
    }


    const student =
        JSON.parse(studentData);


    const category =
        document.getElementById(
            "complaintCategory"
        ).value;

    const location =
        document.getElementById(
            "complaintLocation"
        ).value.trim();

    const priority =
        document.getElementById(
            "complaintPriority"
        ).value;

    const description =
        document.getElementById(
            "complaintDescription"
        ).value.trim();


    if (!category || !description) {

        alert(
            "⚠️ Please select a category and describe the problem."
        );

        return;
    }


    try {

        const response = await fetch(
            "/api/complaints",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    campus_id:
                        student.campus_id,

                    category:
                        category,

                    description:
                        description,

                    location:
                        location,

                    priority:
                        priority
                })
            }
        );


        const data =
            await response.json();


        if (data.success) {

            alert(
                "✅ Complaint submitted successfully!\n\n" +
                "Complaint ID: #" +
                data.complaint_id
            );


            // Clear form

            document.getElementById(
                "complaintCategory"
            ).value = "";

            document.getElementById(
                "complaintLocation"
            ).value = "";

            document.getElementById(
                "complaintPriority"
            ).value = "Normal";

            document.getElementById(
                "complaintDescription"
            ).value = "";


            closeComplaints();

        } else {

            alert(
                "❌ " + data.message
            );
        }

    } catch (error) {

        console.error(error);

        alert(
            "⚠️ Server connection problem.\n" +
            "Please make sure Flask server is running."
        );
    }
}


// ==========================================
// CLOSE COMPLAINT MODAL
// WHEN CLICKING OUTSIDE
// ==========================================

window.addEventListener(
    "click",
    function(event) {

        const modal =
            document.getElementById(
                "complaintModal"
            );

        if (
            event.target === modal
        ) {

            closeComplaints();
        }
    }
);
// ==========================================
// ADMIN LOGIN
// ==========================================

function openAdminLogin() {
    document.getElementById("adminLoginModal").classList.add("active");
}

function closeAdminLogin() {
    document.getElementById("adminLoginModal").classList.remove("active");
}
async function adminLogin() {

    const adminId = document.getElementById("adminId").value.trim();
    const password = document.getElementById("adminPassword").value.trim();
    const message = document.getElementById("adminLoginMessage");

    if (!adminId || !password) {
        message.innerHTML = "⚠️ Please enter Admin ID and Password.";
        return;
    }

    try {

        const response = await fetch("/api/admin/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                admin_id: adminId,
                password: password
            })
        });

        const data = await response.json();

        if (data.success) {

            message.innerHTML = "✅ Login successful!";

            setTimeout(() => {
                window.location.href = "/admin.html";
            }, 500);

        } else {

            message.innerHTML = "❌ " + data.message;

        }

    } catch (error) {

        console.error("Admin login error:", error);
        message.innerHTML = "❌ Server connection failed.";

    }
}
// ==========================================
// HERO IMAGE AUTO SLIDER
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    const slides =
        document.querySelectorAll(".hero-slide");

    if (!slides.length) {
        return;
    }

    let currentSlide = 0;

    setInterval(function () {

        slides[currentSlide].classList.remove("active");

        currentSlide++;

        if (currentSlide >= slides.length) {
            currentSlide = 0;
        }

        slides[currentSlide].classList.add("active");

    }, 3000);

});
// ==========================================
// CAMPUS IMAGE AUTO SLIDER
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    const slides =
        document.querySelectorAll(".campus-slide");

    if (!slides.length) {
        return;
    }

    let currentSlide = 0;

    setInterval(function () {

        slides[currentSlide].classList.remove("active");

        currentSlide++;

        if (currentSlide >= slides.length) {
            currentSlide = 0;
        }

        slides[currentSlide].classList.add("active");

    }, 3000);

});