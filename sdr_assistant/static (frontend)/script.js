document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const accountSelect = document.getElementById('accountSelect');
    const generateBtn = document.getElementById('generateBtn');
    const saveBtn = document.getElementById('saveBtn');
    const loader = document.getElementById('loader');
    const industryInsights = document.getElementById('industryInsights');
    const companyInsights = document.getElementById('companyInsights');
    const visionInsights = document.getElementById('visionInsights');
    const recommendedTalkTrack = document.getElementById('recommendedTalkTrack');
    
    // Sample accounts data
    const accounts = [
        { id: 1, name: "Acme Corporation" },
        { id: 2, name: "TechNova Solutions" },
        { id: 3, name: "Global Dynamics" },
        { id: 4, name: "Quantum Innovations" },
        { id: 5, name: "Stellar Networks" }
    ];
    
    // Populate account dropdown
    accounts.forEach(account => {
        const option = document.createElement('option');
        option.value = account.id;
        option.textContent = account.name;
        accountSelect.appendChild(option);
    });
    
    // Generate research button click
    generateBtn.addEventListener('click', function() {
        const selectedAccount = accountSelect.value;
        const accountName = accountSelect.options[accountSelect.selectedIndex].text;
        
        if (!selectedAccount) {
            showNotification('Please select an account first', 'warning');
            return;
        }
        
        // Show loader
        loader.style.display = 'block';
        clearAllInsights();
        
        // Disable buttons during API call
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        
        // Make API call to generate research
        fetch('/api/research', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                account_id: selectedAccount,
                account_name: accountName
            })
        })
        .then(response => response.json())
        .then(data => {
            // Display insights in their respective sections
            industryInsights.textContent = data.industryInsights || '';
            companyInsights.textContent = data.companyInsights || '';
            visionInsights.textContent = data.visionInsights || '';
            recommendedTalkTrack.textContent = data.recommendedTalkTrack || '';
            
            // Enable save button
            saveBtn.disabled = false;
            showNotification('Research generated successfully!', 'success');
        })
        .catch(error => {
            console.error('Error generating research:', error);
            showNotification('Failed to generate research. Please try again.', 'error');
        })
        .finally(() => {
            // Reset button state
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<i class="fas fa-bolt"></i> Generate Research';
            loader.style.display = 'none';
        });
    });
    
    // Save to Airtable button click
    saveBtn.addEventListener('click', function() {
        saveBtn.disabled = true;
        saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
        showNotification('Saving insights to Airtable...', 'info');
        
        // Get all insights
        const insights = {
            industryInsights: industryInsights.textContent,
            companyInsights: companyInsights.textContent,
            visionInsights: visionInsights.textContent,
            recommendedTalkTrack: recommendedTalkTrack.textContent,
            accountId: accountSelect.value,
            accountName: accountSelect.options[accountSelect.selectedIndex].text
        };
        
        // Make API call to save to Airtable
        fetch('/api/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(insights)
        })
        .then(response => response.json())
        .then(data => {
            showNotification('Insights saved to Airtable successfully!', 'success');
        })
        .catch(error => {
            console.error('Error saving to Airtable:', error);
            showNotification('Failed to save to Airtable. Please try again.', 'error');
        })
        .finally(() => {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '<i class="fas fa-save"></i> Save to Airtable';
        });
    });
    
    // Clear all insight containers
    function clearAllInsights() {
        industryInsights.innerHTML = '';
        companyInsights.innerHTML = '';
        visionInsights.innerHTML = '';
        recommendedTalkTrack.innerHTML = '';
    }
    
    // Notification system
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        
        let icon;
        switch (type) {
            case 'success':
                icon = 'fas fa-check-circle';
                break;
            case 'error':
                icon = 'fas fa-exclamation-circle';
                break;
            case 'warning':
                icon = 'fas fa-exclamation-triangle';
                break;
            default:
                icon = 'fas fa-info-circle';
        }
        
        notification.innerHTML = `
            <i class="${icon}"></i>
            <div>${message}</div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
            notification.style.opacity = '1';
        }, 10);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(400px)';
            notification.style.opacity = '0';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
});
