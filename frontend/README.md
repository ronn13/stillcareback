# StillCare Healthcare Frontend

A modern, responsive web application for managing healthcare services, built with HTML5, CSS3, and JavaScript. This frontend provides a comprehensive interface for managing clients, appointments, visits, and invoices for StillCare healthcare service provider.

## Features

### 🏥 **Dashboard**
- Real-time statistics overview
- Total clients, active appointments, today's visits, and pending invoices
- Recent appointments and today's visits lists
- Interactive cards with hover effects

### 👥 **Client Management**
- Complete CRUD operations for client records
- Personal information (name, email, phone, address)
- Care checklist management with 15 predefined care options
- Professional data table with search and filter capabilities

### 📅 **Appointment Management**
- Schedule and manage appointments
- Link appointments to specific clients
- Set start and end times
- Recurring appointment support with frequency options
- Status tracking (scheduled, completed, cancelled, no-show)

### 🏠 **Visit Management**
- Record actual home visits
- Link visits to appointments
- Track actual start/end times
- Checklist completion tracking
- Staff assignment and visit notes
- Duration calculation

### 💰 **Invoice Management**
- Create and manage invoice groups
- Link clients to invoice groups
- Professional invoice tracking

## Design Features

### 🎨 **Modern Healthcare Theme**
- Professional blue color scheme appropriate for healthcare
- Clean, accessible design following healthcare industry standards
- Responsive design that works on all devices
- Smooth animations and hover effects

### 📱 **Responsive Design**
- Mobile-first approach
- Bootstrap 5 framework
- Optimized for tablets and desktops
- Touch-friendly interface

### 🔧 **User Experience**
- Intuitive navigation
- Modal-based forms for data entry
- Real-time validation
- Success/error notifications
- Loading states and feedback

## File Structure

```
frontend/
├── index.html          # Main application page
├── styles.css          # Custom CSS styling
├── script.js           # JavaScript functionality
└── README.md           # This file
```

## Setup Instructions

### 1. **Prerequisites**
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Django backend running on `http://localhost:8000`
- CORS enabled on Django backend

### 2. **Installation**
1. Ensure your Django backend is running
2. Open `index.html` in a web browser
3. Or serve the files using a local web server:
   ```bash
   # Using Python
   python -m http.server 8080
   
   # Using Node.js
   npx serve .
   
   # Using PHP
   php -S localhost:8080
   ```

### 3. **Backend Configuration**
Make sure your Django backend has:
- CORS headers configured
- API endpoints for all CRUD operations
- Proper serializers for JSON responses

## API Endpoints Required

The frontend expects the following API endpoints:

### Dashboard
- `GET /api/dashboard/` - Dashboard statistics
- `GET /api/appointments/recent/` - Recent appointments
- `GET /api/visits/today/` - Today's visits

### Clients
- `GET /api/clients/` - List all clients
- `POST /api/clients/` - Create new client
- `PUT /api/clients/{id}/` - Update client
- `DELETE /api/clients/{id}/` - Delete client

### Appointments
- `GET /api/appointments/` - List all appointments
- `POST /api/appointments/` - Create new appointment
- `PUT /api/appointments/{id}/` - Update appointment
- `DELETE /api/appointments/{id}/` - Delete appointment

### Visits
- `GET /api/visits/` - List all visits
- `POST /api/visits/` - Create new visit
- `PUT /api/visits/{id}/` - Update visit
- `DELETE /api/visits/{id}/` - Delete visit

### Invoices
- `GET /api/invoices/` - List all invoice groups
- `POST /api/invoices/` - Create new invoice group
- `PUT /api/invoices/{id}/` - Update invoice group
- `DELETE /api/invoices/{id}/` - Delete invoice group

## Usage Guide

### Adding a New Client
1. Click "Add New Client" button
2. Fill in personal information
3. Select care checklist items
4. Click "Save Client"

### Scheduling an Appointment
1. Click "Schedule Appointment" button
2. Select a client from the dropdown
3. Set title, start time, and end time
4. Choose status and recurrence options
5. Click "Save Appointment"

### Recording a Visit
1. Click "Record Visit" button
2. Select the associated appointment
3. Enter actual start/end times
4. Assign staff member
5. Complete checklist items
6. Add visit notes
7. Click "Save Visit"

### Managing Invoices
1. Click "Create Invoice Group" button
2. Enter name and description
3. Click "Save Invoice Group"

## Customization

### Colors
The color scheme can be customized by modifying CSS variables in `styles.css`:
```css
:root {
    --primary-color: #2c5aa0;
    --secondary-color: #4a90e2;
    --success-color: #28a745;
    --info-color: #17a2b8;
    --warning-color: #ffc107;
    --danger-color: #dc3545;
}
```

### Checklist Options
Add or modify care checklist options in `script.js`:
```javascript
const CHECKLIST_OPTIONS = [
    { value: 'basic_care', label: 'Basic Care' },
    // Add more options here
];
```

### API Configuration
Update the API base URL in `script.js`:
```javascript
const API_BASE_URL = 'http://your-backend-url/api';
```

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Security Considerations

- Ensure HTTPS is used in production
- Implement proper authentication and authorization
- Validate all user inputs on the backend
- Use CSRF tokens for form submissions
- Sanitize data before displaying

## Performance Optimization

- Minify CSS and JavaScript for production
- Optimize images and assets
- Use CDN for external libraries
- Implement caching strategies
- Enable gzip compression

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Check if Django backend is running
   - Verify API_BASE_URL in script.js
   - Ensure CORS is properly configured

2. **Modal Not Opening**
   - Check Bootstrap JavaScript is loaded
   - Verify modal IDs match function calls

3. **Data Not Loading**
   - Check browser console for errors
   - Verify API endpoints are working
   - Check network tab for failed requests

### Debug Mode
Enable debug logging by adding this to the browser console:
```javascript
localStorage.setItem('debug', 'true');
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the troubleshooting section
- Review the API documentation
- Contact the development team

---

**StillCare Healthcare Frontend** - Professional healthcare management made simple. 