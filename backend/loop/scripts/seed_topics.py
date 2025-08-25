"""Seed the database with initial topics and subtopics."""
import asyncio
from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from loop.db.dao.learning_dao import LearningDAO
from loop.db.models import load_all_models
from loop.settings import settings


BACKEND_TOPICS = {
    "System Design": {
        "description": "Master scalable system architecture patterns and principles for large-scale applications",
        "category": "Architecture",
        "importance_level": "high",
        "icon_emoji": "🏗️",
        "subtopics": [
            {
                "name": "Scalability Fundamentals",
                "description": "Core principles of horizontal and vertical scaling, load distribution, and capacity planning",
                "order_index": 1,
                "estimated_time_minutes": 20,
                "difficulty_level": 3,
            },
            {
                "name": "Database Scaling Patterns",
                "description": "Sharding, read replicas, CQRS, and database partitioning strategies",
                "order_index": 2,
                "estimated_time_minutes": 25,
                "difficulty_level": 4,
            },
            {
                "name": "Caching Strategies",
                "description": "Multi-layer caching, cache invalidation, CDNs, and distributed caching patterns",
                "order_index": 3,
                "estimated_time_minutes": 18,
                "difficulty_level": 3,
            },
            {
                "name": "Microservices Architecture",
                "description": "Service decomposition, API gateways, service mesh, and inter-service communication",
                "order_index": 4,
                "estimated_time_minutes": 30,
                "difficulty_level": 4,
            },
            {
                "name": "Consistency and CAP Theorem",
                "description": "Eventual consistency, distributed consensus, and trade-offs in distributed systems",
                "order_index": 5,
                "estimated_time_minutes": 22,
                "difficulty_level": 5,
            }
        ]
    },
    
    "Docker Mastery": {
        "description": "Advanced containerization with Docker for production environments",
        "category": "DevOps",
        "importance_level": "high", 
        "icon_emoji": "🐳",
        "subtopics": [
            {
                "name": "Multi-stage Build Optimization",
                "description": "Efficient Dockerfiles, layer caching, and minimal image creation techniques",
                "order_index": 1,
                "estimated_time_minutes": 15,
                "difficulty_level": 2,
            },
            {
                "name": "Docker Networking Deep Dive",
                "description": "Custom networks, overlay networks, and container-to-container communication",
                "order_index": 2,
                "estimated_time_minutes": 20,
                "difficulty_level": 3,
            },
            {
                "name": "Volume Management and Persistence",
                "description": "Data persistence strategies, bind mounts vs volumes, and backup patterns",
                "order_index": 3,
                "estimated_time_minutes": 18,
                "difficulty_level": 3,
            },
            {
                "name": "Security Best Practices",
                "description": "Container security scanning, non-root users, secrets management, and hardening",
                "order_index": 4,
                "estimated_time_minutes": 25,
                "difficulty_level": 4,
            },
            {
                "name": "Production Deployment Patterns",
                "description": "Health checks, rolling updates, resource limits, and monitoring containers",
                "order_index": 5,
                "estimated_time_minutes": 22,
                "difficulty_level": 4,
            }
        ]
    },
    
    "PostgreSQL Advanced": {
        "description": "Expert-level PostgreSQL performance, optimization, and administration",
        "category": "Database",
        "importance_level": "high",
        "icon_emoji": "🐘",
        "subtopics": [
            {
                "name": "Query Optimization and Indexing",
                "description": "Index types, query planning, EXPLAIN analysis, and performance tuning",
                "order_index": 1,
                "estimated_time_minutes": 25,
                "difficulty_level": 4,
            },
            {
                "name": "Advanced SQL and Window Functions",
                "description": "CTEs, window functions, JSON operations, and complex query patterns",
                "order_index": 2,
                "estimated_time_minutes": 20,
                "difficulty_level": 3,
            },
            {
                "name": "Replication and High Availability",
                "description": "Streaming replication, failover, read replicas, and backup strategies",
                "order_index": 3,
                "estimated_time_minutes": 30,
                "difficulty_level": 5,
            },
            {
                "name": "Connection Pooling and Scaling",
                "description": "PgBouncer, connection management, and horizontal scaling techniques",
                "order_index": 4,
                "estimated_time_minutes": 18,
                "difficulty_level": 4,
            },
            {
                "name": "Monitoring and Performance Tuning",
                "description": "pg_stat views, performance monitoring, and database optimization strategies",
                "order_index": 5,
                "estimated_time_minutes": 22,
                "difficulty_level": 4,
            }
        ]
    },
    
    "Kubernetes Operations": {
        "description": "Production Kubernetes management, troubleshooting, and advanced patterns",
        "category": "DevOps",
        "importance_level": "high",
        "icon_emoji": "☸️",
        "subtopics": [
            {
                "name": "Pod Lifecycle and Troubleshooting",
                "description": "Pod states, restart policies, debugging failed pods, and resource management",
                "order_index": 1,
                "estimated_time_minutes": 20,
                "difficulty_level": 3,
            },
            {
                "name": "Service Discovery and Ingress",
                "description": "Services, endpoints, ingress controllers, and traffic routing patterns",
                "order_index": 2,
                "estimated_time_minutes": 25,
                "difficulty_level": 4,
            },
            {
                "name": "ConfigMaps, Secrets, and Security",
                "description": "Configuration management, secret handling, RBAC, and security policies",
                "order_index": 3,
                "estimated_time_minutes": 22,
                "difficulty_level": 4,
            },
            {
                "name": "StatefulSets and Persistent Storage",
                "description": "Stateful applications, persistent volumes, and data management in Kubernetes",
                "order_index": 4,
                "estimated_time_minutes": 28,
                "difficulty_level": 5,
            },
            {
                "name": "Monitoring and Observability",
                "description": "Prometheus, Grafana, logging strategies, and cluster monitoring",
                "order_index": 5,
                "estimated_time_minutes": 25,
                "difficulty_level": 4,
            }
        ]
    },
    
    "API Design Excellence": {
        "description": "REST API best practices, GraphQL, and modern API patterns for scalable systems",
        "category": "Backend Development",
        "importance_level": "medium-high",
        "icon_emoji": "🔌",
        "subtopics": [
            {
                "name": "RESTful Design Principles",
                "description": "HTTP methods, status codes, resource modeling, and REST maturity levels",
                "order_index": 1,
                "estimated_time_minutes": 18,
                "difficulty_level": 2,
            },
            {
                "name": "API Versioning Strategies",
                "description": "URL versioning, header versioning, backward compatibility, and deprecation",
                "order_index": 2,
                "estimated_time_minutes": 15,
                "difficulty_level": 3,
            },
            {
                "name": "Authentication and Authorization",
                "description": "JWT, OAuth2, API keys, rate limiting, and security best practices",
                "order_index": 3,
                "estimated_time_minutes": 25,
                "difficulty_level": 4,
            },
            {
                "name": "GraphQL Fundamentals",
                "description": "Schema design, resolvers, queries vs mutations, and N+1 problem solutions",
                "order_index": 4,
                "estimated_time_minutes": 22,
                "difficulty_level": 3,
            },
            {
                "name": "API Documentation and Testing",
                "description": "OpenAPI/Swagger, automated testing, contract testing, and API governance",
                "order_index": 5,
                "estimated_time_minutes": 20,
                "difficulty_level": 3,
            }
        ]
    }
}


async def create_topic_with_subtopics(dao: LearningDAO, topic_name: str, topic_data: Dict) -> None:
    """Create a topic and its subtopics."""
    print(f"Creating topic: {topic_name}")
    
    # Create the topic
    topic = await dao.topics.create_topic(
        name=topic_name,
        description=topic_data["description"],
        category=topic_data["category"],
        importance_level=topic_data["importance_level"],
        estimated_subtopics=len(topic_data["subtopics"]),
        icon_emoji=topic_data.get("icon_emoji"),
    )
    
    # Create subtopics
    for subtopic_data in topic_data["subtopics"]:
        print(f"  Creating subtopic: {subtopic_data['name']}")
        await dao.subtopics.create_subtopic(
            topic_id=topic.id,
            **subtopic_data
        )
    
    print(f"✅ Created topic '{topic_name}' with {len(topic_data['subtopics'])} subtopics")


async def seed_backend_topics() -> None:
    """Seed the database with backend engineering topics."""
    print("🌱 Starting topic seeding process...")
    
    # Load all models first to ensure relationships are properly set up
    load_all_models()
    
    # Create database engine and session
    engine = create_async_engine(str(settings.db_url))
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            dao = LearningDAO(session)
            
            # Check if topics already exist
            existing_topics = await dao.topics.get_topics(limit=1)
            if existing_topics:
                print("⚠️  Topics already exist. Skipping seeding process.")
                return
            
            # Create all topics
            for topic_name, topic_data in BACKEND_TOPICS.items():
                await create_topic_with_subtopics(dao, topic_name, topic_data)
            
            print(f"🎉 Successfully seeded {len(BACKEND_TOPICS)} topics!")
            
        except Exception as e:
            print(f"❌ Error during seeding: {e}")
            raise


async def seed_additional_topics() -> None:
    """Seed additional specialized topics for comprehensive learning."""
    # Load all models first
    load_all_models()
    
    additional_topics = {
        "Redis and Caching": {
            "description": "Advanced Redis patterns, clustering, and distributed caching strategies",
            "category": "Database",
            "importance_level": "medium-high",
            "icon_emoji": "🔴",
            "subtopics": [
                {
                    "name": "Redis Data Structures Mastery",
                    "description": "Strings, hashes, sets, sorted sets, and advanced data structure usage",
                    "order_index": 1,
                    "estimated_time_minutes": 20,
                    "difficulty_level": 3,
                },
                {
                    "name": "Redis Clustering and High Availability",
                    "description": "Redis Cluster, Sentinel, replication, and failover strategies",
                    "order_index": 2,
                    "estimated_time_minutes": 25,
                    "difficulty_level": 4,
                },
                {
                    "name": "Cache Invalidation Patterns",
                    "description": "TTL strategies, cache-aside, write-through, and distributed invalidation",
                    "order_index": 3,
                    "estimated_time_minutes": 18,
                    "difficulty_level": 4,
                }
            ]
        },
        
        "Message Queues and Event Streaming": {
            "description": "Asynchronous processing with RabbitMQ, Kafka, and event-driven architectures",
            "category": "Architecture", 
            "importance_level": "medium-high",
            "icon_emoji": "📨",
            "subtopics": [
                {
                    "name": "Message Queue Fundamentals",
                    "description": "Producer-consumer patterns, queue types, and reliability guarantees",
                    "order_index": 1,
                    "estimated_time_minutes": 18,
                    "difficulty_level": 2,
                },
                {
                    "name": "Apache Kafka Deep Dive",
                    "description": "Partitioning, consumer groups, exactly-once processing, and stream processing",
                    "order_index": 2,
                    "estimated_time_minutes": 30,
                    "difficulty_level": 4,
                },
                {
                    "name": "Event-Driven Architecture Patterns",
                    "description": "Event sourcing, CQRS, saga patterns, and distributed transactions",
                    "order_index": 3,
                    "estimated_time_minutes": 25,
                    "difficulty_level": 5,
                }
            ]
        }
    }
    
    # Create database engine and session  
    engine = create_async_engine(str(settings.db_url))
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            dao = LearningDAO(session)
            
            for topic_name, topic_data in additional_topics.items():
                await create_topic_with_subtopics(dao, topic_name, topic_data)
            
            print(f"🎉 Successfully seeded {len(additional_topics)} additional topics!")
            
        except Exception as e:
            print(f"❌ Error during additional seeding: {e}")
            raise


if __name__ == "__main__":
    print("🚀 Running topic seeding script...")
    asyncio.run(seed_backend_topics())
    asyncio.run(seed_additional_topics())