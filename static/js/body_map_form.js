document.addEventListener('DOMContentLoaded', function() {
    // Consent fields
    const consentGivenCheckbox = document.getElementById('id_consent_given');
    const consentTypeField = document.getElementById('id_consent_type');
    
    // Photography fields
    const photographyConsentCheckbox = document.getElementById('id_photography_consent');
    const photosTakenCheckbox = document.getElementById('id_photos_taken');
    const photoDocumentationField = document.getElementById('id_photo_documentation');
    
    // Referral fields
    const medicalReferralCheckbox = document.getElementById('id_medical_referral');
    const medicalReferralDetailsField = document.getElementById('id_medical_referral_details');
    
    const policeNotifiedCheckbox = document.getElementById('id_police_notified');
    const policeNotificationDetailsField = document.getElementById('id_police_notification_details');
    
    const safeguardingReferralCheckbox = document.getElementById('id_safeguarding_referral');
    const safeguardingReferralDetailsField = document.getElementById('id_safeguarding_referral_details');
    
    // Follow-up fields
    const followUpRequiredCheckbox = document.getElementById('id_follow_up_required');
    const followUpDetailsField = document.getElementById('id_follow_up_details');
    
    // Function to toggle consent fields
    function toggleConsentFields() {
        if (consentGivenCheckbox && consentTypeField) {
            const isChecked = consentGivenCheckbox.checked;
            const consentTypeContainer = consentTypeField.closest('.form-group') || consentTypeField.parentElement;
            
            if (isChecked) {
                consentTypeContainer.style.display = 'block';
                consentTypeField.required = true;
                
                const label = consentTypeContainer.querySelector('label');
                if (label && !label.textContent.includes('*')) {
                    label.textContent += ' *';
                }
            } else {
                consentTypeContainer.style.display = 'none';
                consentTypeField.required = false;
                consentTypeField.value = '';
                
                const label = consentTypeContainer.querySelector('label');
                if (label) {
                    label.textContent = label.textContent.replace(' *', '');
                }
            }
        }
    }
    
    // Function to toggle photography fields
    function togglePhotographyFields() {
        if (photographyConsentCheckbox && photosTakenCheckbox && photoDocumentationField) {
            const consentChecked = photographyConsentCheckbox.checked;
            const photosTakenChecked = photosTakenCheckbox.checked;
            
            const photosTakenContainer = photosTakenCheckbox.closest('.form-group') || photosTakenCheckbox.parentElement;
            const photoDocContainer = photoDocumentationField.closest('.form-group') || photoDocumentationField.parentElement;
            
            // Show/hide photos taken checkbox based on consent
            if (consentChecked) {
                photosTakenContainer.style.display = 'block';
            } else {
                photosTakenContainer.style.display = 'none';
                photosTakenCheckbox.checked = false;
            }
            
            // Show/hide photo documentation based on photos taken
            if (photosTakenChecked) {
                photoDocContainer.style.display = 'block';
                photoDocumentationField.required = true;
                
                const label = photoDocContainer.querySelector('label');
                if (label && !label.textContent.includes('*')) {
                    label.textContent += ' *';
                }
            } else {
                photoDocContainer.style.display = 'none';
                photoDocumentationField.required = false;
                photoDocumentationField.value = '';
                
                const label = photoDocContainer.querySelector('label');
                if (label) {
                    label.textContent = label.textContent.replace(' *', '');
                }
            }
        }
    }
    
    // Function to toggle referral fields
    function toggleReferralFields() {
        // Medical referral
        if (medicalReferralCheckbox && medicalReferralDetailsField) {
            const isChecked = medicalReferralCheckbox.checked;
            const container = medicalReferralDetailsField.closest('.form-group') || medicalReferralDetailsField.parentElement;
            
            if (isChecked) {
                container.style.display = 'block';
                medicalReferralDetailsField.required = true;
                
                const label = container.querySelector('label');
                if (label && !label.textContent.includes('*')) {
                    label.textContent += ' *';
                }
            } else {
                container.style.display = 'none';
                medicalReferralDetailsField.required = false;
                medicalReferralDetailsField.value = '';
                
                const label = container.querySelector('label');
                if (label) {
                    label.textContent = label.textContent.replace(' *', '');
                }
            }
        }
        
        // Police notification
        if (policeNotifiedCheckbox && policeNotificationDetailsField) {
            const isChecked = policeNotifiedCheckbox.checked;
            const container = policeNotificationDetailsField.closest('.form-group') || policeNotificationDetailsField.parentElement;
            
            if (isChecked) {
                container.style.display = 'block';
                policeNotificationDetailsField.required = true;
                
                const label = container.querySelector('label');
                if (label && !label.textContent.includes('*')) {
                    label.textContent += ' *';
                }
            } else {
                container.style.display = 'none';
                policeNotificationDetailsField.required = false;
                policeNotificationDetailsField.value = '';
                
                const label = container.querySelector('label');
                if (label) {
                    label.textContent = label.textContent.replace(' *', '');
                }
            }
        }
        
        // Safeguarding referral
        if (safeguardingReferralCheckbox && safeguardingReferralDetailsField) {
            const isChecked = safeguardingReferralCheckbox.checked;
            const container = safeguardingReferralDetailsField.closest('.form-group') || safeguardingReferralDetailsField.parentElement;
            
            if (isChecked) {
                container.style.display = 'block';
                safeguardingReferralDetailsField.required = true;
                
                const label = container.querySelector('label');
                if (label && !label.textContent.includes('*')) {
                    label.textContent += ' *';
                }
            } else {
                container.style.display = 'none';
                safeguardingReferralDetailsField.required = false;
                safeguardingReferralDetailsField.value = '';
                
                const label = container.querySelector('label');
                if (label) {
                    label.textContent = label.textContent.replace(' *', '');
                }
            }
        }
    }
    
    // Function to toggle follow-up fields
    function toggleFollowUpFields() {
        if (followUpRequiredCheckbox && followUpDetailsField) {
            const isChecked = followUpRequiredCheckbox.checked;
            const container = followUpDetailsField.closest('.form-group') || followUpDetailsField.parentElement;
            
            if (isChecked) {
                container.style.display = 'block';
                followUpDetailsField.required = true;
                
                const label = container.querySelector('label');
                if (label && !label.textContent.includes('*')) {
                    label.textContent += ' *';
                }
            } else {
                container.style.display = 'none';
                followUpDetailsField.required = false;
                followUpDetailsField.value = '';
                
                const label = container.querySelector('label');
                if (label) {
                    label.textContent = label.textContent.replace(' *', '');
                }
            }
        }
    }
    
    // Set initial states
    toggleConsentFields();
    togglePhotographyFields();
    toggleReferralFields();
    toggleFollowUpFields();
    
    // Add event listeners
    if (consentGivenCheckbox) {
        consentGivenCheckbox.addEventListener('change', toggleConsentFields);
    }
    
    if (photographyConsentCheckbox) {
        photographyConsentCheckbox.addEventListener('change', togglePhotographyFields);
    }
    
    if (photosTakenCheckbox) {
        photosTakenCheckbox.addEventListener('change', togglePhotographyFields);
    }
    
    if (medicalReferralCheckbox) {
        medicalReferralCheckbox.addEventListener('change', toggleReferralFields);
    }
    
    if (policeNotifiedCheckbox) {
        policeNotifiedCheckbox.addEventListener('change', toggleReferralFields);
    }
    
    if (safeguardingReferralCheckbox) {
        safeguardingReferralCheckbox.addEventListener('change', toggleReferralFields);
    }
    
    if (followUpRequiredCheckbox) {
        followUpRequiredCheckbox.addEventListener('change', toggleFollowUpFields);
    }
}); 