# Eqiupment System

## Overview

The equipment management system will be a valuable tool provided by the CSXL lab to undergraduate students with a passion for technology. 
This system enables undergraduates to check, checkout, or reserve equipment for their academic and professional development activities.
Additionally, this feature will be integrated into the preexisting CSXL website, allowing for more control over functionality by staff members.

## Implmentation Notes

### Overview

The equipment checkout feature is a full-stack application composed of an `Angular` frontend, Python `FastAPI` backend, and `PostgreSQL` database. 
The implementation revolves around two data models: `Equipment` and `Reservations`. 

The `Equipment` model includes data such as - equipment ID, name, type of equipment, availability, and a data value for any special notes about that equipment. 

The `Reservations` model includes data such as reservation ID, type of equipment, the user who checked out equipment, equipment, and a data value for any special notes about the reservation. 

If the end user were to want to check out equipment, a reservation would be created on their behalf with the data filled using data from them and from the equipment they wish to check out.

### Design Choices

With CSXL already using a data model for `user` to hold important needed to identify a student, this feature encapsulates a user data model within the `reservations` data model to streamline integration. By using the data within the user model, this feature is able to create reservations by accessing that data directly, allowing for less implementation needed for functionality.

Additionally, by separating the models into `equipment` and `reservations`, it allows for the design of an admin-only mode, which can interact with the equipment database more directly, allowing for adding/modifying of equipment by staff members. This implementation then allowed the reservations data model to be geared towards individual student use, allowing for a more polished data model, which was important for development streamlining.

### Development Concerns

As this feature was built on the preexisting csxl website, any changes to the original code could impact the functionality of this feature. For example, if the `user` model was changed to remove its capability to store first/last names, only needing PID to access UNC's database to pull that information when needed, this feature would lose the ability to display that information for the end user.

For new developers working on expanding this feature, familiarize yourself to the reservations and equipment data models in the backend. These data models are then used to format the Postgre database using SQL alchemy, found in `backend/services/equipment` and `backend/services/reservation`. 

These files mentioned earlier also contain the methods called by the FastAPI HTTP routes found in `backend/api/equipment` and `backend/api/reservation`. Additional functionality on the database level can be added by writing additional methods in those respective files.

### Future Work

Given the limited scope for this feature in both timeline and labor pool, this feature can be improved upon. One notable area for improvement is the data stored within the `reservations` model. In the current implementation, the front-end UI allows a student to view their current reservations but does not allow them to see the time they checked it out as that data is not being stored. If that data were stored, it can be used to limit the timeframe equipment is able to be checked out, allow other users to hold that equipment for future use after its current reservation is over, and many other functions.

The management of equipment is another area that can be expanded upon. Currently if an equipment is marked as unavailable, it can't be edited in the database in an effort to prevent equipment that is reserved from being changed. This has the effect of not having the ability to mark equipment as unavailable outside of placing it into a reservation as there is no way to edit it. Adding more status codes to differentiate an item being reserved versus other statuses is likely the most straightforward way to solve this issue.
