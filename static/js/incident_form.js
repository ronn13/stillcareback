document.addEventListener('DOMContentLoaded', function() {
    const wasPersonInjuredCheckbox = document.getElementById('id_was_person_injured');
    const personInjuredField = document.getElementById('id_person_injured');
    const injuryDetailsField = document.getElementById('id_injury_details');
    
    const incidentNotifiableRiddorCheckbox = document.getElementById('id_incident_notifiable_riddor');
    const f2508DocumentField = document.getElementById('id_f2508_document');
    
    if (wasPersonInjuredCheckbox && personInjuredField && injuryDetailsField) {
        // Function to toggle injury field visibility and requirement
        function toggleInjuryFields() {
            const isChecked = wasPersonInjuredCheckbox.checked;
            
            // Get the parent containers for styling
            const personInjuredContainer = personInjuredField.closest('.form-group') || personInjuredField.parentElement;
            const injuryDetailsContainer = injuryDetailsField.closest('.form-group') || injuryDetailsField.parentElement;
            
            if (isChecked) {
                // Show fields and make them required
                personInjuredContainer.style.display = 'block';
                injuryDetailsContainer.style.display = 'block';
                personInjuredField.required = true;
                injuryDetailsField.required = true;
                
                // Add visual indication that fields are required
                const personInjuredLabel = personInjuredContainer.querySelector('label');
                const injuryDetailsLabel = injuryDetailsContainer.querySelector('label');
                
                if (personInjuredLabel && !personInjuredLabel.textContent.includes('*')) {
                    personInjuredLabel.textContent += ' *';
                }
                if (injuryDetailsLabel && !injuryDetailsLabel.textContent.includes('*')) {
                    injuryDetailsLabel.textContent += ' *';
                }
            } else {
                // Hide fields and make them not required
                personInjuredContainer.style.display = 'none';
                injuryDetailsContainer.style.display = 'none';
                personInjuredField.required = false;
                injuryDetailsField.required = false;
                
                // Clear the fields when hidden
                personInjuredField.value = '';
                injuryDetailsField.value = '';
                
                // Remove visual indication
                const personInjuredLabel = personInjuredContainer.querySelector('label');
                const injuryDetailsLabel = injuryDetailsContainer.querySelector('label');
                
                if (personInjuredLabel) {
                    personInjuredLabel.textContent = personInjuredLabel.textContent.replace(' *', '');
                }
                if (injuryDetailsLabel) {
                    injuryDetailsLabel.textContent = injuryDetailsLabel.textContent.replace(' *', '');
                }
            }
        }
        
        // Set initial state for injury fields
        toggleInjuryFields();
        
        // Add event listener for injury checkbox changes
        wasPersonInjuredCheckbox.addEventListener('change', toggleInjuryFields);
    }
    
    if (incidentNotifiableRiddorCheckbox && f2508DocumentField) {
        // Function to toggle F2508 document field visibility and requirement
        function toggleF2508Field() {
            const isChecked = incidentNotifiableRiddorCheckbox.checked;
            
            // Get the parent container for styling
            const f2508Container = f2508DocumentField.closest('.form-group') || f2508DocumentField.parentElement;
            
            if (isChecked) {
                // Show field and make it required
                f2508Container.style.display = 'block';
                f2508DocumentField.required = true;
                
                // Add visual indication that field is required
                const f2508Label = f2508Container.querySelector('label');
                if (f2508Label && !f2508Label.textContent.includes('*')) {
                    f2508Label.textContent += ' *';
                }
            } else {
                // Hide field and make it not required
                f2508Container.style.display = 'none';
                f2508DocumentField.required = false;
                
                // Clear the field when hidden
                f2508DocumentField.value = '';
                
                // Remove visual indication
                const f2508Label = f2508Container.querySelector('label');
                if (f2508Label) {
                    f2508Label.textContent = f2508Label.textContent.replace(' *', '');
                }
            }
        }
        
        // Set initial state for F2508 field
        toggleF2508Field();
        
        // Add event listener for RIDDOR checkbox changes
        incidentNotifiableRiddorCheckbox.addEventListener('change', toggleF2508Field);
    }
}); 