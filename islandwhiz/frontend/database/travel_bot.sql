-- Create Database
CREATE DATABASE travel_bot;
USE travel_bot;

-- Destination Table
CREATE TABLE Destination (
    DestinationID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Description TEXT,
    Location VARCHAR(100),
    Type VARCHAR(50),
    Country VARCHAR(50),
    Region VARCHAR(50)
);

-- Travel Advice Table
CREATE TABLE TravelAdvice (
    AdviceID INT PRIMARY KEY AUTO_INCREMENT,
    DestinationID INT,
    AdviceDescription TEXT,
    DateAdded DATE,
    FOREIGN KEY (DestinationID) REFERENCES Destination(DestinationID)
);

-- Best Time to Visit Table
CREATE TABLE BestTimeToVisit (
    TimeID INT PRIMARY KEY AUTO_INCREMENT,
    DestinationID INT,
    BestSeason VARCHAR(50),
    RecommendedMonth VARCHAR(50),
    TemperatureRange VARCHAR(50),
    FOREIGN KEY (DestinationID) REFERENCES Destination(DestinationID)
);

-- Live Info Table
CREATE TABLE LiveInfo (
    InfoID INT PRIMARY KEY AUTO_INCREMENT,
    DestinationID INT,
    LiveStatus VARCHAR(50),
    UpdateTime DATETIME,
    Description TEXT,
    FOREIGN KEY (DestinationID) REFERENCES Destination(DestinationID)
);


-- Insert Dummy Data into Destination
INSERT INTO Destination (Name, Description, Location, Type, Country, Region) VALUES
('Ella', 'A beautiful hill station surrounded by lush greenery and tea plantations.', 'Uva Province', 'Hill Station', 'Sri Lanka', 'Uva'),
('Mirissa', 'A beach town known for whale watching and golden sandy beaches.', 'Southern Province', 'Beach', 'Sri Lanka', 'Southern'),
('Sigiriya', 'Ancient rock fortress with frescoes and panoramic views.', 'Central Province', 'Heritage Site', 'Sri Lanka', 'Central');

-- Insert Dummy Data into TravelAdvice
INSERT INTO TravelAdvice (DestinationID, AdviceDescription, DateAdded) VALUES
(1, 'Carry light jackets; evenings in Ella can be chilly.', '2024-10-01'),
(2, 'Best to swim only in marked safe zones due to strong currents.', '2024-12-05'),
(3, 'Climb Sigiriya Rock early in the morning to avoid heat and crowds.', '2024-09-20');

-- Insert Dummy Data into BestTimeToVisit
INSERT INTO BestTimeToVisit (DestinationID, BestSeason, RecommendedMonth, TemperatureRange) VALUES
(1, 'Cool & Dry', 'January to March', '15°C - 25°C'),
(2, 'Dry Season', 'December to April', '27°C - 33°C'),
(3, 'Mild & Dry', 'February to April', '25°C - 30°C');

-- Insert Dummy Data into LiveInfo
INSERT INTO LiveInfo (DestinationID, LiveStatus, UpdateTime, Description) VALUES
(1, 'Open', NOW(), 'Train services are operating normally. Weather is clear.'),
(2, 'Partially Open', NOW(), 'Beach access allowed but strong tides today. Lifeguards on alert.'),
(3, 'Open', NOW(), 'Sigiriya Rock entry is open. Wear comfortable shoes for hiking.');