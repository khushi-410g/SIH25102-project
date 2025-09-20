CREATE SCHEMA IF NOT EXISTS student_dashboard;

CREATE TABLE IF NOT EXISTS student_dashboard.students (
    student_id SERIAL PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(10),
    enrollment_date DATE,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS student_dashboard.attendance (
    attendance_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES student_dashboard.students(student_id) ON DELETE CASCADE,
    attendance_date DATE NOT NULL,
    attendance_percentage NUMERIC(5, 2) CHECK (attendance_percentage >= 0 AND attendance_percentage <= 100),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS student_dashboard.assessments (
    assessment_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES student_dashboard.students(student_id) ON DELETE CASCADE,
    subject VARCHAR(50) NOT NULL,
    test_date DATE NOT NULL,
    score NUMERIC(5, 2) CHECK (score >= 0 AND score <= 100),
    max_score NUMERIC(5, 2) DEFAULT 100,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS student_dashboard.fees (
    fee_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES student_dashboard.students(student_id) ON DELETE CASCADE,
    payment_date DATE NOT NULL,
    amount_paid NUMERIC(10, 2) NOT NULL,
    fee_status VARCHAR(20) CHECK (fee_status IN ('Paid', 'Partial', 'Pending')),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS student_dashboard.metadata (
    metadata_id SERIAL PRIMARY KEY,
    upload_timestamp TIMESTAMP DEFAULT NOW(),
    source_name VARCHAR(100),
    file_name VARCHAR(255),
    record_count INT,
    description TEXT
);
