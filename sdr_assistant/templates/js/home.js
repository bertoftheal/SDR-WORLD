// SDR World Home Dashboard
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard
    initDashboard();
    
    // Setup event listeners
    setupEventListeners();
});

// Initialize dashboard with widgets
function initDashboard() {
    const dashboardContainer = document.getElementById('dashboard-widgets');
    
    // Define widget data
    const widgets = [
        // Row 1: Priority widgets
        {
            id: 'notifications-widget',
            title: 'Notifications',
            icon: 'fa-bell',
            colClass: 'col-lg-6 col-md-6',
            content: generateNotificationsContent()
        },
        {
            id: 'tasks-widget',
            title: 'Today\'s Tasks',
            icon: 'fa-tasks',
            colClass: 'col-lg-6 col-md-6',
            content: generateTasksContent()
        },
        
        // Row 2: Calendar and Metrics
        {
            id: 'calendar-widget',
            title: 'Calendar',
            icon: 'fa-calendar-alt',
            colClass: 'col-lg-8 col-md-8',
            content: generateCalendarContent()
        },
        {
            id: 'metrics-widget',
            title: 'Key Metrics',
            icon: 'fa-chart-line',
            colClass: 'col-lg-4 col-md-4',
            content: generateMetricsContent()
        },
        
        // Row 3: Secondary widgets
        {
            id: 'accounts-widget',
            title: 'Quick Access Accounts',
            icon: 'fa-users',
            colClass: 'col-lg-4 col-md-4',
            content: generateAccountsContent()
        },
        {
            id: 'templates-widget',
            title: 'Communication Templates',
            icon: 'fa-envelope',
            colClass: 'col-lg-4 col-md-4',
            content: generateTemplatesContent()
        },
        {
            id: 'news-widget',
            title: 'News & Insights',
            icon: 'fa-newspaper',
            colClass: 'col-lg-4 col-md-4',
            content: generateNewsContent()
        }
    ];
    
    // Build and append widgets
    widgets.forEach(widget => {
        const widgetHTML = `
            <div class="${widget.colClass}">
                <div class="dashboard-widget p-4 rounded shadow-sm bg-white" id="${widget.id}">
                    <div class="widget-header d-flex align-items-center mb-3">
                        <div class="widget-icon me-3 text-white p-2 rounded" style="background-color: #06b6a2;">
                            <i class="fas ${widget.icon} fa-lg"></i>
                        </div>
                        <h3 class="mb-0 fs-5 fw-bold">${widget.title}</h3>
                        <div class="dropdown ms-auto">
                            <button class="btn btn-link text-muted" type="button" data-bs-toggle="dropdown">
                                <i class="fas fa-ellipsis-v"></i>
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end">
                                <li><a class="dropdown-item" href="#"><i class="fas fa-sync-alt me-2"></i>Refresh</a></li>
                                <li><a class="dropdown-item" href="#"><i class="fas fa-cog me-2"></i>Configure</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="#"><i class="fas fa-times me-2"></i>Hide widget</a></li>
                            </ul>
                        </div>
                    </div>
                    <div class="widget-content">
                        ${widget.content}
                    </div>
                </div>
            </div>
        `;
        
        dashboardContainer.innerHTML += widgetHTML;
    });
    
    // Initialize any charts in the metrics widget
    initializeCharts();
}

// Setup event listeners for widgets
function setupEventListeners() {
    // Task completion toggle
    document.querySelectorAll('.task-check').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const taskItem = this.closest('.task-item');
            if (this.checked) {
                taskItem.classList.add('completed');
            } else {
                taskItem.classList.remove('completed');
            }
        });
    });
    
    // Meeting join buttons
    document.querySelectorAll('.join-meeting-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            alert('Joining meeting: ' + this.getAttribute('data-meeting'));
        });
    });
}

// Generate content for Notifications widget
function generateNotificationsContent() {
    return `
        <div class="notifications-list">
            <div class="notification-item d-flex align-items-start mb-3 pb-3 border-bottom">
                <div class="notification-icon me-3 text-danger">
                    <i class="fas fa-exclamation-circle"></i>
                </div>
                <div class="notification-content">
                    <p class="mb-1 fw-bold">Follow up with Acme Corp</p>
                    <p class="text-muted small mb-1">Your follow-up is 2 days overdue</p>
                    <p class="small text-muted">10 minutes ago</p>
                </div>
            </div>
            <div class="notification-item d-flex align-items-start mb-3 pb-3 border-bottom">
                <div class="notification-icon me-3 text-primary">
                    <i class="fas fa-user-plus"></i>
                </div>
                <div class="notification-content">
                    <p class="mb-1 fw-bold">New lead assigned: Technova Inc.</p>
                    <p class="text-muted small mb-1">Added by Mark Johnson</p>
                    <p class="small text-muted">2 hours ago</p>
                </div>
            </div>
            <div class="notification-item d-flex align-items-start mb-3 pb-3 border-bottom">
                <div class="notification-icon me-3 text-success">
                    <i class="fas fa-calendar-check"></i>
                </div>
                <div class="notification-content">
                    <p class="mb-1 fw-bold">Meeting confirmed with Global Tech</p>
                    <p class="text-muted small mb-1">Tomorrow at 2:30 PM</p>
                    <p class="small text-muted">5 hours ago</p>
                </div>
            </div>
            <div class="notification-item d-flex align-items-start">
                <div class="notification-icon me-3 text-info">
                    <i class="fas fa-bell"></i>
                </div>
                <div class="notification-content">
                    <p class="mb-1 fw-bold">Research completed for DataSphere</p>
                    <p class="text-muted small mb-1">AI-generated research ready to review</p>
                    <p class="small text-muted">Yesterday</p>
                </div>
            </div>
        </div>
        <div class="text-end mt-3">
            <a href="#" class="text-decoration-none" style="color: #06b6a2;">View all notifications <i class="fas fa-arrow-right ms-1"></i></a>
        </div>
    `;
}

// Generate content for Tasks widget
function generateTasksContent() {
    return `
        <div class="tasks-list">
            <div class="task-item d-flex align-items-center mb-3 pb-2 border-bottom">
                <input type="checkbox" class="form-check-input task-check me-3" id="task1">
                <label for="task1" class="form-check-label flex-grow-1">
                    <span class="fw-bold d-block">Call John at Microsoft</span>
                    <span class="text-muted small">Discuss integration opportunities</span>
                </label>
                <span class="badge bg-danger me-2">High</span>
                <span class="text-muted small">11:00 AM</span>
            </div>
            <div class="task-item d-flex align-items-center mb-3 pb-2 border-bottom">
                <input type="checkbox" class="form-check-input task-check me-3" id="task2">
                <label for="task2" class="form-check-label flex-grow-1">
                    <span class="fw-bold d-block">Follow up with Cisco</span>
                    <span class="text-muted small">Send product comparison sheet</span>
                </label>
                <span class="badge bg-warning text-dark me-2">Medium</span>
                <span class="text-muted small">1:30 PM</span>
            </div>
            <div class="task-item d-flex align-items-center mb-3 pb-2 border-bottom">
                <input type="checkbox" class="form-check-input task-check me-3" id="task3">
                <label for="task3" class="form-check-label flex-grow-1">
                    <span class="fw-bold d-block">Research NVIDIA developments</span>
                    <span class="text-muted small">Check recent press releases</span>
                </label>
                <span class="badge bg-primary me-2">Normal</span>
                <span class="text-muted small">3:00 PM</span>
            </div>
            <div class="task-item d-flex align-items-center mb-3 pb-2 border-bottom">
                <input type="checkbox" class="form-check-input task-check me-3" id="task4">
                <label for="task4" class="form-check-label flex-grow-1">
                    <span class="fw-bold d-block">Update CRM notes</span>
                    <span class="text-muted small">Add notes from today's calls</span>
                </label>
                <span class="badge bg-secondary me-2">Low</span>
                <span class="text-muted small">4:45 PM</span>
            </div>
        </div>
        <div class="d-flex justify-content-between align-items-center mt-3">
            <a href="#" class="btn btn-sm" style="background-color: #06b6a2; color: white;"><i class="fas fa-plus me-1"></i> Add Task</a>
            <a href="#" class="text-decoration-none" style="color: #06b6a2;">View all tasks <i class="fas fa-arrow-right ms-1"></i></a>
        </div>
    `;
}

// Generate content for Calendar widget
function generateCalendarContent() {
    return `
        <div class="calendar-view mb-3">
            <h4 class="fw-bold mb-3 fs-6">Today's Schedule</h4>
            <div class="calendar-events">
                <div class="event-item d-flex mb-3 pb-2 border-bottom">
                    <div class="event-time text-center me-3" style="min-width: 80px;">
                        <span class="d-block fw-bold">10:00 AM</span>
                        <span class="small text-muted">45 min</span>
                    </div>
                    <div class="event-content p-2 rounded flex-grow-1" style="background-color: rgba(6, 182, 162, 0.1);">
                        <div class="d-flex justify-content-between align-items-start">
                            <h5 class="fs-6 mb-1 fw-bold">Discovery Call - TechForge Inc.</h5>
                            <button class="btn btn-sm join-meeting-btn" data-meeting="TechForge" style="background-color: #06b6a2; color: white;"><i class="fas fa-video me-1"></i> Join</button>
                        </div>
                        <p class="mb-1 small">Meeting with CTO about AI implementation</p>
                        <div class="d-flex align-items-center">
                            <span class="me-3 small"><i class="fas fa-user me-1"></i> Robert Chen</span>
                            <span class="small"><i class="fas fa-map-marker-alt me-1"></i> Zoom</span>
                        </div>
                    </div>
                </div>
                <div class="event-item d-flex mb-3 pb-2 border-bottom">
                    <div class="event-time text-center me-3" style="min-width: 80px;">
                        <span class="d-block fw-bold">1:30 PM</span>
                        <span class="small text-muted">30 min</span>
                    </div>
                    <div class="event-content p-2 rounded flex-grow-1" style="background-color: rgba(108, 117, 125, 0.1);">
                        <div class="d-flex justify-content-between align-items-start">
                            <h5 class="fs-6 mb-1 fw-bold">Follow-up Demo - Acme Corp</h5>
                            <button class="btn btn-sm join-meeting-btn" data-meeting="Acme" style="background-color: #06b6a2; color: white;"><i class="fas fa-video me-1"></i> Join</button>
                        </div>
                        <p class="mb-1 small">Product demo of new features</p>
                        <div class="d-flex align-items-center">
                            <span class="me-3 small"><i class="fas fa-user me-1"></i> Sarah Williams</span>
                            <span class="small"><i class="fas fa-map-marker-alt me-1"></i> Teams</span>
                        </div>
                    </div>
                </div>
                <div class="event-item d-flex">
                    <div class="event-time text-center me-3" style="min-width: 80px;">
                        <span class="d-block fw-bold">3:45 PM</span>
                        <span class="small text-muted">15 min</span>
                    </div>
                    <div class="event-content p-2 rounded flex-grow-1" style="background-color: rgba(220, 53, 69, 0.1);">
                        <div class="d-flex justify-content-between align-items-start">
                            <h5 class="fs-6 mb-1 fw-bold">Sales Team Sync</h5>
                            <button class="btn btn-sm join-meeting-btn" data-meeting="SalesSync" style="background-color: #06b6a2; color: white;"><i class="fas fa-video me-1"></i> Join</button>
                        </div>
                        <p class="mb-1 small">Weekly team check-in</p>
                        <div class="d-flex align-items-center">
                            <span class="me-3 small"><i class="fas fa-users me-1"></i> Sales Team</span>
                            <span class="small"><i class="fas fa-map-marker-alt me-1"></i> Google Meet</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="d-flex justify-content-between align-items-center mt-3">
            <button class="btn btn-sm" style="background-color: #06b6a2; color: white;"><i class="fas fa-plus me-1"></i> Schedule Meeting</button>
            <a href="#" class="text-decoration-none" style="color: #06b6a2;">Full calendar <i class="fas fa-arrow-right ms-1"></i></a>
        </div>
    `;
}

// Generate content for Metrics widget
function generateMetricsContent() {
    return `
        <div class="metrics-summary mb-4">
            <div class="row g-3">
                <div class="col-6">
                    <div class="metric-card p-2 rounded bg-light">
                        <p class="small text-muted mb-1">Calls Today</p>
                        <h4 class="fw-bold mb-0">8/12</h4>
                        <div class="progress mt-2" style="height: 5px;">
                            <div class="progress-bar" role="progressbar" style="width: 66%; background-color: #06b6a2;" aria-valuenow="66" aria-valuemin="0" aria-valuemax="100"></div>
                        </div>
                    </div>
                </div>
                <div class="col-6">
                    <div class="metric-card p-2 rounded bg-light">
                        <p class="small text-muted mb-1">Emails Sent</p>
                        <h4 class="fw-bold mb-0">15/20</h4>
                        <div class="progress mt-2" style="height: 5px;">
                            <div class="progress-bar" role="progressbar" style="width: 75%; background-color: #06b6a2;" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"></div>
                        </div>
                    </div>
                </div>
                <div class="col-6">
                    <div class="metric-card p-2 rounded bg-light">
                        <p class="small text-muted mb-1">Meetings Set</p>
                        <h4 class="fw-bold mb-0">3</h4>
                        <p class="small text-success mb-0"><i class="fas fa-arrow-up me-1"></i> 50% vs. last week</p>
                    </div>
                </div>
                <div class="col-6">
                    <div class="metric-card p-2 rounded bg-light">
                        <p class="small text-muted mb-1">Response Rate</p>
                        <h4 class="fw-bold mb-0">28%</h4>
                        <p class="small text-danger mb-0"><i class="fas fa-arrow-down me-1"></i> 5% vs. last week</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="chart-container">
            <canvas id="weeklyActivityChart" height="150"></canvas>
        </div>
    `;
}

// Generate content for Accounts widget
function generateAccountsContent() {
    return `
        <div class="accounts-list">
            <div class="account-item d-flex align-items-center mb-3 pb-2 border-bottom">
                <div class="account-logo rounded-circle me-3 d-flex align-items-center justify-content-center" style="width: 40px; height: 40px; background-color: #f8f9fa;">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Nvidia_logo.svg/1200px-Nvidia_logo.svg.png" alt="NVIDIA" class="img-fluid" style="max-width: 70%; max-height: 70%;">
                </div>
                <div class="account-details flex-grow-1">
                    <h5 class="mb-0 fs-6 fw-bold">NVIDIA</h5>
                    <p class="text-muted small mb-0">Last contact: Yesterday</p>
                </div>
                <div class="account-action">
                    <button class="btn btn-sm rounded-circle" style="background-color: #06b6a2; color: white;"><i class="fas fa-arrow-right"></i></button>
                </div>
            </div>
            <div class="account-item d-flex align-items-center mb-3 pb-2 border-bottom">
                <div class="account-logo rounded-circle me-3 d-flex align-items-center justify-content-center" style="width: 40px; height: 40px; background-color: #f8f9fa;">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Cisco_logo_blue_2016.svg/1200px-Cisco_logo_blue_2016.svg.png" alt="Cisco" class="img-fluid" style="max-width: 70%; max-height: 70%;">
                </div>
                <div class="account-details flex-grow-1">
                    <h5 class="mb-0 fs-6 fw-bold">Cisco Systems</h5>
                    <p class="text-muted small mb-0">Last contact: 2 days ago</p>
                </div>
                <div class="account-action">
                    <button class="btn btn-sm rounded-circle" style="background-color: #06b6a2; color: white;"><i class="fas fa-arrow-right"></i></button>
                </div>
            </div>
            <div class="account-item d-flex align-items-center mb-3 pb-2 border-bottom">
                <div class="account-logo rounded-circle me-3 d-flex align-items-center justify-content-center" style="width: 40px; height: 40px; background-color: #f8f9fa;">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Microsoft_logo.svg/1200px-Microsoft_logo.svg.png" alt="Microsoft" class="img-fluid" style="max-width: 70%; max-height: 70%;">
                </div>
                <div class="account-details flex-grow-1">
                    <h5 class="mb-0 fs-6 fw-bold">Microsoft</h5>
                    <p class="text-muted small mb-0">Last contact: 3 days ago</p>
                </div>
                <div class="account-action">
                    <button class="btn btn-sm rounded-circle" style="background-color: #06b6a2; color: white;"><i class="fas fa-arrow-right"></i></button>
                </div>
            </div>
        </div>
        <div class="text-end mt-3">
            <a href="accounts.html" class="text-decoration-none" style="color: #06b6a2;">View all accounts <i class="fas fa-arrow-right ms-1"></i></a>
        </div>
    `;
}

// Generate content for Templates widget
function generateTemplatesContent() {
    return `
        <div class="templates-list">
            <div class="template-item mb-3 pb-2 border-bottom">
                <div class="d-flex justify-content-between align-items-start">
                    <h5 class="fs-6 mb-1 fw-bold">Product Demo Follow-up</h5>
                    <span class="badge bg-success">90% Response</span>
                </div>
                <p class="text-muted small mb-2">Thank you for taking the time to join our product demo yesterday...</p>
                <button class="btn btn-sm" style="background-color: #06b6a2; color: white;"><i class="fas fa-copy me-1"></i> Copy</button>
            </div>
            <div class="template-item mb-3 pb-2 border-bottom">
                <div class="d-flex justify-content-between align-items-start">
                    <h5 class="fs-6 mb-1 fw-bold">Initial Outreach</h5>
                    <span class="badge bg-primary">70% Response</span>
                </div>
                <p class="text-muted small mb-2">I noticed your company has been expanding into the AI space...</p>
                <button class="btn btn-sm" style="background-color: #06b6a2; color: white;"><i class="fas fa-copy me-1"></i> Copy</button>
            </div>
            <div class="template-item">
                <div class="d-flex justify-content-between align-items-start">
                    <h5 class="fs-6 mb-1 fw-bold">Meeting Request</h5>
                    <span class="badge bg-warning text-dark">55% Response</span>
                </div>
                <p class="text-muted small mb-2">I'd like to schedule a 15-minute call to discuss how our solution...</p>
                <button class="btn btn-sm" style="background-color: #06b6a2; color: white;"><i class="fas fa-copy me-1"></i> Copy</button>
            </div>
        </div>
        <div class="text-end mt-3">
            <a href="#" class="text-decoration-none" style="color: #06b6a2;">View all templates <i class="fas fa-arrow-right ms-1"></i></a>
        </div>
    `;
}

// Generate content for News widget
function generateNewsContent() {
    return `
        <div class="news-list">
            <div class="news-item mb-3 pb-2 border-bottom">
                <span class="badge bg-danger mb-1">NVIDIA</span>
                <h5 class="fs-6 mb-1 fw-bold">NVIDIA Announces New AI Chips</h5>
                <p class="text-muted small mb-1">Revolutionary new architecture claims 4x performance increase...</p>
                <p class="small text-muted">2 hours ago • <a href="#" class="text-decoration-none" style="color: #06b6a2;">Read more</a></p>
            </div>
            <div class="news-item mb-3 pb-2 border-bottom">
                <span class="badge bg-primary mb-1">Microsoft</span>
                <h5 class="fs-6 mb-1 fw-bold">Microsoft Expands Cloud Services</h5>
                <p class="text-muted small mb-1">New data centers opening in Asia and Europe...</p>
                <p class="small text-muted">Yesterday • <a href="#" class="text-decoration-none" style="color: #06b6a2;">Read more</a></p>
            </div>
            <div class="news-item">
                <span class="badge bg-success mb-1">Industry</span>
                <h5 class="fs-6 mb-1 fw-bold">Tech Spending Expected to Rise in Q3</h5>
                <p class="text-muted small mb-1">Analysts predict 15% increase in enterprise tech budgets...</p>
                <p class="small text-muted">2 days ago • <a href="#" class="text-decoration-none" style="color: #06b6a2;">Read more</a></p>
            </div>
        </div>
        <div class="text-end mt-3">
            <a href="#" class="text-decoration-none" style="color: #06b6a2;">View all news <i class="fas fa-arrow-right ms-1"></i></a>
        </div>
    `;
}

// Initialize charts
function initializeCharts() {
    // Weekly activity chart
    const activityCtx = document.getElementById('weeklyActivityChart');
    if (activityCtx) {
        new Chart(activityCtx, {
            type: 'bar',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
                datasets: [
                    {
                        label: 'Calls',
                        data: [12, 8, 10, 11, 8],
                        backgroundColor: '#06b6a2',
                        borderColor: '#06b6a2',
                        borderWidth: 1
                    },
                    {
                        label: 'Emails',
                        data: [20, 15, 18, 22, 15],
                        backgroundColor: '#71e9d8',
                        borderColor: '#71e9d8',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            boxWidth: 10
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            maxTicksLimit: 5
                        }
                    }
                }
            }
        });
    }
}
