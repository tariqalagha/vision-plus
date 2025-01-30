using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;

var builder = WebApplication.CreateBuilder(args);

// Add services
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddCors();

var app = builder.Build();

// Configure middleware
app.UseHttpsRedirection();
app.UseCors(x => x.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader());
app.UseStaticFiles();

// Define routes
app.MapGet("/", () => "Vision+ Medical Imaging System");
app.MapGet("/api/health", () => "System is healthy");
app.MapGet("/api/version", () => new { Version = "1.0.0", Developer = "Dr. Tariq Alagha" });
app.MapGet("/api/status", () => new { Status = "Online", Timestamp = DateTime.UtcNow });

// Enable Swagger in development
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.Run();