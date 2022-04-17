drop table if exists Item;
drop table if exists User;
drop table if exists Bid;
drop table if exists Item_Category;

create table Item(
    ID INT,
    Name VARCHAR,
    Currently FLOAT,
    Buy_Price FLOAT,
    First_Bid FLOAT,
    Number_of_Bids INT,
    Started DATE,
    Ends Date,
    Seller INT,
    Description VARCHAR
);
create table User(
    UserID VARCHAR,
    Location VARCHAR,
    Country VARCHAR,
    Rating VARCHAR
);
create table Bid(
    ItemID INT,
    BidderID VARCHAR,
    Time Date,
    Amount FLOAT
);
create table Item_Category(
    ItemID INT,
    Category VARCHAR
);